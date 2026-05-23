-- configura mysql secondary para replicar desde mysql primary
-- este script se ejecuta en mysql secondary

STOP REPLICA;

RESET REPLICA ALL;

CHANGE REPLICATION SOURCE TO
  SOURCE_HOST='mysql-primary',
  SOURCE_PORT=3306,
  SOURCE_USER='replica_user',
  SOURCE_PASSWORD='replica_pass',
  SOURCE_AUTO_POSITION=1,
  GET_SOURCE_PUBLIC_KEY=1;

START REPLICA;

SHOW REPLICA STATUS\G
