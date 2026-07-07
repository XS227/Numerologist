<?php

declare(strict_types=1);

/**
 * Vipps eCommerce v2 callback router.
 *
 * Vipps POSTs to:  {callbackPrefix}/v2/payments/{orderId}
 * Our prefix is:   https://numerologist.setai.no/vipps
 * So full path is: /vipps/v2/payments/{orderId}
 *
 * This file is served for ALL /vipps/* requests by nginx.
 * It handles:
 *   POST /vipps/v2/payments/{orderId}   — transaction status callback
 *   GET  /vipps/v2/payments/{orderId}   — (same path, ignore)
 */

require_once dirname(__DIR__) . '/includes/config.php';
require_once dirname(__DIR__) . '/includes/db.php';
require_once dirname(__DIR__) . '/includes/mail.php';

// Parse orderId from REQUEST_URI
// Expected path: /vipps/v2/payments/{orderId}
$uri     = (string) ($_SERVER['REQUEST_URI'] ?? '');
$uriPath = strtok($uri, '?');
$matches = [];
if (!preg_match('#^/vipps/v2/payments/([A-Za-z0-9_\-]+)#', $uriPath, $matches)) {
    // Unknown sub-path under /vipps/ — return 404
    http_response_code(404);
    header('Content-Type: application/json');
    echo json_encode(['error' => 'not found']);
    exit;
}
$orderId = $matches[1];

// Vipps only sends POST for callbacks
$method = strtoupper((string) ($_SERVER['REQUEST_METHOD'] ?? 'GET'));
if ($method !== 'POST') {
    http_response_code(405);
    header('Content-Type: application/json');
    echo json_encode(['error' => 'method not allowed']);
    exit;
}

// Read + validate Authorization header
// Vipps sends: Authorization: authToken {our_auth_token}
$authHeader = (string) ($_SERVER['HTTP_AUTHORIZATION'] ?? '');
$tokenFromHeader = '';
if (preg_match('/^authToken\s+(\S+)$/i', $authHeader, $m)) {
    $tokenFromHeader = $m[1];
}

// Load order
$order = get_order($orderId);
if ($order === null) {
    http_response_code(200); // Acknowledge to Vipps even if order unknown
    header('Content-Type: application/json');
    echo json_encode(['status' => 'ignored', 'reason' => 'order not found']);
    exit;
}

// Verify auth token
$storedToken = (string) ($order['vipps_auth_token'] ?? '');
if ($storedToken !== '' && !hash_equals($storedToken, $tokenFromHeader)) {
    error_log("Vipps callback: invalid auth token for order {$orderId}");
    http_response_code(401);
    header('Content-Type: application/json');
    echo json_encode(['error' => 'unauthorized']);
    exit;
}

// Read JSON body
$rawBody = (string) file_get_contents('php://input');
$payload = [];
if ($rawBody !== '') {
    try {
        $payload = json_decode($rawBody, true, 8, JSON_THROW_ON_ERROR);
    } catch (JsonException $e) {
        error_log("Vipps callback: invalid JSON for order {$orderId}: " . $e->getMessage());
    }
}

// Extract transaction status
// Vipps v2 payload: { orderId, transactionInfo: { status, ... }, ... }
$transactionInfo = $payload['transactionInfo'] ?? $payload['transaction'] ?? [];
$vippsStatus     = strtolower((string) ($transactionInfo['status'] ?? $payload['transactionInfo']['status'] ?? ''));
$vippsOrderId    = (string) ($payload['orderId'] ?? $orderId);

// Map Vipps statuses to our statuses
$paymentStatus = match($vippsStatus) {
    'reserved', 'sale', 'captured'       => 'paid',
    'cancel', 'cancelled', 'void'        => 'cancelled',
    'failed', 'rejected', 'autoreversal' => 'failed',
    default                              => 'pending',
};

// Only process each order once to avoid double-emails
if ($order['payment_status'] !== 'paid' && $paymentStatus === 'paid') {
    update_order_payment($orderId, 'paid', $vippsOrderId);

    // Reload updated order for email
    $updatedOrder = get_order($orderId);
    if ($updatedOrder !== null) {
        try {
            send_order_confirmation($updatedOrder);
        } catch (Throwable $e) {
            error_log("Vipps callback: mail failed for {$orderId}: " . $e->getMessage());
        }
    }

    error_log("Vipps callback: order {$orderId} marked paid (Vipps status: {$vippsStatus})");

} elseif ($paymentStatus !== 'pending') {
    update_order_payment($orderId, $paymentStatus, $vippsOrderId);
    error_log("Vipps callback: order {$orderId} status → {$paymentStatus}");
}

// Vipps expects HTTP 200 with empty or JSON body
http_response_code(200);
header('Content-Type: application/json');
echo json_encode(['status' => 'ok']);
