-- crea el usuario que usa mysql para replicar datos
-- este script se ejecuta en mysql primary

CREATE USER IF NOT EXISTS 'replica_user'@'%' IDENTIFIED BY 'replica_pass';

GRANT REPLICATION SLAVE, REPLICATION CLIENT ON *.* TO 'replica_user'@'%';

FLUSH PRIVILEGES;

SELECT user, host
FROM mysql.user
WHERE user = 'replica_user';
