<?php

declare(strict_types=1);

require_once __DIR__ . '/config.php';

function db(): PDO
{
    static $pdo = null;
    if ($pdo !== null) return $pdo;

    $dir = dirname((string) DB_PATH);
    if (!is_dir($dir)) {
        mkdir($dir, 0750, true);
        chown($dir, 'www-data');
    }

    $pdo = new PDO('sqlite:' . DB_PATH, options: [
        PDO::ATTR_ERRMODE            => PDO::ERRMODE_EXCEPTION,
        PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
    ]);

    $pdo->exec('PRAGMA journal_mode=WAL; PRAGMA foreign_keys=ON;');

    $pdo->exec(<<<'SQL'
        CREATE TABLE IF NOT EXISTS orders (
            id               TEXT     PRIMARY KEY,
            package          TEXT     NOT NULL,
            price_ore        INTEGER  NOT NULL,
            birth_name       TEXT     NOT NULL,
            current_name     TEXT     NOT NULL,
            birth_date       TEXT     NOT NULL,
            sex              TEXT     NOT NULL,
            address          TEXT     NOT NULL,
            phone            TEXT     NOT NULL,
            email            TEXT     NOT NULL,
            payment_status   TEXT     NOT NULL DEFAULT 'pending',
            vipps_order_id   TEXT,
            vipps_auth_token TEXT,
            analysis_status  TEXT     NOT NULL DEFAULT 'pending',
            created_at       TEXT     NOT NULL
                             DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now'))
        )
    SQL);

    return $pdo;
}

function generate_order_id(): string
{
    // Format: NUM + unix timestamp + 4 random uppercase alphanum chars (~30 chars max)
    $rand = strtoupper(substr(bin2hex(random_bytes(4)), 0, 6));
    return 'NUM' . time() . $rand;
}

function save_order(array $data): string
{
    $id = generate_order_id();
    db()->prepare(<<<'SQL'
        INSERT INTO orders
            (id, package, price_ore, birth_name, current_name, birth_date,
             sex, address, phone, email, vipps_auth_token)
        VALUES
            (:id, :package, :price_ore, :birth_name, :current_name, :birth_date,
             :sex, :address, :phone, :email, :vipps_auth_token)
    SQL)->execute([
        ':id'               => $id,
        ':package'          => $data['package'],
        ':price_ore'        => $data['price_ore'],
        ':birth_name'       => $data['birth_name'],
        ':current_name'     => $data['current_name'],
        ':birth_date'       => $data['birth_date'],
        ':sex'              => $data['sex'],
        ':address'          => $data['address'],
        ':phone'            => $data['phone'],
        ':email'            => $data['email'],
        ':vipps_auth_token' => $data['vipps_auth_token'],
    ]);
    return $id;
}

function get_order(string $id): ?array
{
    $stmt = db()->prepare('SELECT * FROM orders WHERE id = :id');
    $stmt->execute([':id' => $id]);
    $row = $stmt->fetch();
    return $row ?: null;
}

function update_order_payment(string $id, string $status, string $vippsOrderId = ''): void
{
    db()->prepare(
        'UPDATE orders SET payment_status = :s, vipps_order_id = :v WHERE id = :id'
    )->execute([':s' => $status, ':v' => $vippsOrderId, ':id' => $id]);
}
