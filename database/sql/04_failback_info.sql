-- failback secondary hacia primary
-- este archivo documenta el proceso sql de recuperacion
-- el dump se genera desde secondary
-- luego se restaura en primary
-- esto permite que primary recupere los datos guardados en secondary durante la falla

-- paso 1 en secondary
-- mysqldump cajero_atm desde secondary

-- paso 2 en primary
-- restaurar el dump sobre la base cajero_atm

-- paso 3 en secondary
-- ejecutar 03_configurar_replica.sql para volver a replicar primary hacia secondary

-- verificacion recomendada en ambas bases

USE cajero_atm;

SELECT numero_cuenta, saldo, tipo_cuenta
FROM cuentas;

SELECT id, tipo, monto, saldo_anterior, saldo_nuevo, fecha
FROM transacciones
ORDER BY id DESC
LIMIT 10;

SELECT id, categoria, accion, nodo_bd, fecha
FROM auditorias
ORDER BY id DESC
LIMIT 10;
