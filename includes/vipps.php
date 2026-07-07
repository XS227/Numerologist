<?php

declare(strict_types=1);

require_once __DIR__ . '/config.php';

final class Vipps
{
    private static ?string $cachedToken  = null;
    private static int     $tokenExpires = 0;

    // ── Access token ──────────────────────────────────────────────────────────

    private static function token(): string
    {
        if (self::$cachedToken !== null && time() < self::$tokenExpires) {
            return self::$cachedToken;
        }

        [$body, $status] = self::request(
            'POST',
            VIPPS_BASE_URL . '/accesstoken/get',
            [],
            '{}',
            [
                'client_id: '     . VIPPS_CLIENT_ID,
                'client_secret: ' . VIPPS_CLIENT_SECRET,
                'Ocp-Apim-Subscription-Key: ' . VIPPS_SUBSCRIPTION_KEY,
                'Content-Type: application/json',
            ]
        );

        if ($status !== 200) {
            throw new RuntimeException("Vipps: token fetch failed (HTTP {$status}): {$body}");
        }

        $data = json_decode($body, true, 8, JSON_THROW_ON_ERROR);
        self::$cachedToken  = (string) $data['access_token'];
        self::$tokenExpires = time() + max(0, (int) $data['expires_in']) - 60;

        return self::$cachedToken;
    }

    // ── Public API ────────────────────────────────────────────────────────────

    /**
     * Initiate a Vipps eCommerce payment.
     *
     * @return string  The Vipps redirect URL (send the user there).
     */
    public static function initiatePayment(
        string $orderId,
        int    $amountOre,
        string $transactionText,
        string $phone,
        string $authToken
    ): string {
        $callbackBase = SITE_URL . '/vipps';
        $fallback     = SITE_URL . '/bestill/takk.php?orderId=' . rawurlencode($orderId);

        $payload = [
            'merchantInfo' => [
                'merchantSerialNumber' => VIPPS_MSN,
                'callbackPrefix'       => $callbackBase,
                'fallBack'             => $fallback,
                'authToken'            => $authToken,
                'isApp'                => false,
            ],
            'customerInfo' => [
                'mobileNumber' => self::normalisePhone($phone),
            ],
            'transaction' => [
                'orderId'         => $orderId,
                'amount'          => $amountOre,
                'transactionText' => mb_substr($transactionText, 0, 100),
                'skipLandingPage' => false,
            ],
        ];

        [$body, $status] = self::request(
            'POST',
            VIPPS_BASE_URL . '/ecomm/v2/payments',
            self::authHeaders(),
            json_encode($payload, JSON_THROW_ON_ERROR | JSON_UNESCAPED_UNICODE)
        );

        if ($status !== 202) {
            throw new RuntimeException("Vipps: payment init failed (HTTP {$status}): {$body}");
        }

        $data = json_decode($body, true, 8, JSON_THROW_ON_ERROR);
        return (string) $data['url'];
    }

    /**
     * Fetch full payment details for an order.
     */
    public static function paymentDetails(string $orderId): array
    {
        $url = VIPPS_BASE_URL . '/ecomm/v2/payments/' . rawurlencode($orderId) . '/details';
        [$body, $status] = self::request('GET', $url, self::authHeaders());

        if ($status !== 200) {
            throw new RuntimeException("Vipps: get details failed (HTTP {$status}): {$body}");
        }

        return json_decode($body, true, 8, JSON_THROW_ON_ERROR);
    }

    // ── Helpers ───────────────────────────────────────────────────────────────

    private static function authHeaders(): array
    {
        return [
            'Authorization: Bearer ' . self::token(),
            'Ocp-Apim-Subscription-Key: ' . VIPPS_SUBSCRIPTION_KEY,
            'Merchant-Serial-Number: ' . VIPPS_MSN,
            'X-Request-Id: ' . self::uuid4(),
            'X-Timestamp: ' . gmdate('Y-m-d\TH:i:s\Z'),
            'Content-Type: application/json',
            'Accept: application/json',
        ];
    }

    /**
     * @return array{string, int}  [response body, HTTP status]
     */
    private static function request(
        string $method,
        string $url,
        array  $headers = [],
        string $body    = '',
        ?array $overrideHeaders = null
    ): array {
        $ch = curl_init($url);
        curl_setopt_array($ch, [
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_TIMEOUT        => 15,
            CURLOPT_CUSTOMREQUEST  => $method,
            CURLOPT_HTTPHEADER     => $overrideHeaders ?? $headers,
            CURLOPT_SSL_VERIFYPEER => true,
        ]);
        if ($body !== '' && in_array($method, ['POST', 'PUT', 'PATCH'], true)) {
            curl_setopt($ch, CURLOPT_POSTFIELDS, $body);
        }

        $response = (string) curl_exec($ch);
        $status   = (int) curl_getinfo($ch, CURLINFO_HTTP_CODE);
        $err      = curl_error($ch);
        curl_close($ch);

        if ($err !== '') {
            throw new RuntimeException("Vipps: cURL error: {$err}");
        }

        return [$response, $status];
    }

    private static function normalisePhone(string $phone): string
    {
        $digits = preg_replace('/\D/', '', $phone);
        // Strip Norwegian country code (47) if present and result is 10 digits
        if (strlen($digits) === 10 && str_starts_with($digits, '47')) {
            $digits = substr($digits, 2);
        }
        return $digits;
    }

    private static function uuid4(): string
    {
        $bytes = random_bytes(16);
        $bytes[6] = chr((ord($bytes[6]) & 0x0f) | 0x40);
        $bytes[8] = chr((ord($bytes[8]) & 0x3f) | 0x80);
        return vsprintf('%s%s-%s-%s-%s-%s%s%s', str_split(bin2hex($bytes), 4));
    }
}
