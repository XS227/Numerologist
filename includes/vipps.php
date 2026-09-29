<?php

declare(strict_types=1);

require_once __DIR__ . '/config.php';

final class Vipps
{
    private static ?string $cachedToken  = null;
    private static int     $tokenExpires = 0;

    private static function token(): string
    {
        if (self::$cachedToken !== null && time() < self::$tokenExpires) {
            return self::$cachedToken;
        }

        [$body, $status] = self::request(
            'POST',
            VIPPS_BASE_URL . '/accesstoken/get',
            [],
            '',
            [
                'client_id: ' . VIPPS_CLIENT_ID,
                'client_secret: ' . VIPPS_CLIENT_SECRET,
                'Ocp-Apim-Subscription-Key: ' . VIPPS_SUBSCRIPTION_KEY,
                'Merchant-Serial-Number: ' . VIPPS_MSN,
                'Vipps-System-Name: Numerologist',
                'Vipps-System-Version: 1.0.0',
                'Vipps-System-Plugin-Name: Numerologist-Custom',
                'Vipps-System-Plugin-Version: 1.0.0',
                'Content-Type: application/json',
            ]
        );

        if ($status !== 200) {
            throw new RuntimeException("Vipps: token fetch failed (HTTP {$status}): {$body}");
        }

        $data = json_decode($body, true, 8, JSON_THROW_ON_ERROR);
        self::$cachedToken  = (string) ($data['access_token'] ?? '');
        self::$tokenExpires = time() + max(0, (int) ($data['expires_in'] ?? 3600)) - 60;
        if (self::$cachedToken === '') {
            throw new RuntimeException('Vipps: token response did not contain access_token');
        }

        return self::$cachedToken;
    }

    /**
     * Create a Vipps MobilePay ePayment using WEB_REDIRECT.
     *
     * @return string Redirect URL returned by Vipps.
     */
    public static function initiatePayment(
        string $orderId,
        int    $amountOre,
        string $transactionText,
        string $phone,
        string $authToken
    ): string {
        unset($authToken); // Legacy eCom callback token; ePayment uses polling/webhooks.

        $returnUrl = SITE_URL . '/bestill/takk.php?orderId=' . rawurlencode($orderId);
        $payload = [
            'amount' => [
                'value' => $amountOre,
                'currency' => 'NOK',
            ],
            'paymentMethod' => [
                'type' => 'WALLET',
            ],
            'reference' => $orderId,
            'paymentDescription' => mb_substr($transactionText, 0, 100),
            'returnUrl' => $returnUrl,
            'userFlow' => 'WEB_REDIRECT',
        ];

        $msisdn = self::normaliseMsisdn($phone);
        if ($msisdn !== '') {
            $payload['customer'] = ['phoneNumber' => $msisdn];
        }

        [$body, $status] = self::request(
            'POST',
            VIPPS_BASE_URL . '/epayment/v1/payments',
            self::authHeaders('create-' . $orderId),
            json_encode($payload, JSON_THROW_ON_ERROR | JSON_UNESCAPED_UNICODE)
        );

        if ($status !== 201) {
            throw new RuntimeException("Vipps: payment init failed (HTTP {$status}): {$body}");
        }

        $data = json_decode($body, true, 8, JSON_THROW_ON_ERROR);
        $redirectUrl = (string) ($data['redirectUrl'] ?? '');
        if ($redirectUrl === '') {
            throw new RuntimeException('Vipps: payment response did not contain redirectUrl');
        }
        return $redirectUrl;
    }

    public static function paymentDetails(string $orderId): array
    {
        $url = VIPPS_BASE_URL . '/epayment/v1/payments/' . rawurlencode($orderId);
        [$body, $status] = self::request('GET', $url, self::authHeaders());

        if ($status !== 200) {
            throw new RuntimeException("Vipps: get payment failed (HTTP {$status}): {$body}");
        }

        return json_decode($body, true, 8, JSON_THROW_ON_ERROR);
    }

    public static function capturePayment(string $orderId, int $amountOre): array
    {
        $url = VIPPS_BASE_URL . '/epayment/v1/payments/' . rawurlencode($orderId) . '/capture';
        $payload = [
            'modificationAmount' => [
                'value' => $amountOre,
                'currency' => 'NOK',
            ],
        ];
        [$body, $status] = self::request(
            'POST',
            $url,
            self::authHeaders('capture-' . $orderId),
            json_encode($payload, JSON_THROW_ON_ERROR)
        );

        if ($status !== 200) {
            throw new RuntimeException("Vipps: capture failed (HTTP {$status}): {$body}");
        }

        return json_decode($body, true, 8, JSON_THROW_ON_ERROR);
    }

    private static function authHeaders(?string $idempotencyKey = null): array
    {
        $headers = [
            'Authorization: Bearer ' . self::token(),
            'Ocp-Apim-Subscription-Key: ' . VIPPS_SUBSCRIPTION_KEY,
            'Merchant-Serial-Number: ' . VIPPS_MSN,
            'Vipps-System-Name: Numerologist',
            'Vipps-System-Version: 1.0.0',
            'Vipps-System-Plugin-Name: Numerologist-Custom',
            'Vipps-System-Plugin-Version: 1.0.0',
            'Content-Type: application/json',
            'Accept: application/json',
        ];
        if ($idempotencyKey !== null && $idempotencyKey !== '') {
            $headers[] = 'Idempotency-Key: ' . substr($idempotencyKey, 0, 50);
        }
        return $headers;
    }

    /**
     * @return array{string, int}
     */
    private static function request(
        string $method,
        string $url,
        array  $headers = [],
        string $body = '',
        ?array $overrideHeaders = null
    ): array {
        $ch = curl_init($url);
        curl_setopt_array($ch, [
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_TIMEOUT => 15,
            CURLOPT_CUSTOMREQUEST => $method,
            CURLOPT_HTTPHEADER => $overrideHeaders ?? $headers,
            CURLOPT_SSL_VERIFYPEER => true,
        ]);
        if (in_array($method, ['POST', 'PUT', 'PATCH'], true)) {
            curl_setopt($ch, CURLOPT_POSTFIELDS, $body);
        }

        $response = (string) curl_exec($ch);
        $status = (int) curl_getinfo($ch, CURLINFO_HTTP_CODE);
        $err = curl_error($ch);
        curl_close($ch);

        if ($err !== '') {
            throw new RuntimeException("Vipps: cURL error: {$err}");
        }

        return [$response, $status];
    }

    private static function normaliseMsisdn(string $phone): string
    {
        $digits = (string) preg_replace('/\D/', '', $phone);
        if (strlen($digits) === 8) {
            return '47' . $digits;
        }
        if (strlen($digits) === 10 && str_starts_with($digits, '47')) {
            return $digits;
        }
        return '';
    }
}
