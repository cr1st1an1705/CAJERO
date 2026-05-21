FROM mysql:8.4

COPY failover_monitor_container.sh /usr/local/bin/failover_monitor_container.sh

RUN chmod +x /usr/local/bin/failover_monitor_container.sh

CMD ["failover_monitor_container.sh"]
