
create user monitor;
SET PASSWORD FOR monitor = PASSWORD('monitor');
USE monitor;
grant all on monitor to monitor@localhost;
GRANT ALL ON monitor.* TO monitor@localhost IDENTIFIED BY 'monitor';
GRANT ALL ON monitor.* TO monitor@'%' IDENTIFIED BY 'monitor';
flush privileges;
