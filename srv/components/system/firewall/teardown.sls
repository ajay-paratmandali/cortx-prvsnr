include:
  - .start

Remove public-data-zone:
  cmd.run:
    - name: firewall-cmd --permanent --delete-zone=public-data-zone

Remove private-data-zone:
  cmd.run:
    - name: firewall-cmd --permanent --delete-zone=private-data-zone

Remove management-zone:
  cmd.run:
    - name: firewall-cmd --permanent --delete-zone=management-zone

# Ensure ssh works when the firwall servcie starts for the next time
{% if 'mgmt0' in grains['ip4_interfaces'] and grains['ip4_interfaces']['mgmt0'] %}
  {%- set mgmt_if = 'mgmt0' -%}
{% else %}
  {%- set mgmt_if = pillar['cluster'][grains['id']]['network']['mgmt_nw']['iface'][0] -%}
{%- endif -%}
public:
  firewalld.present:
    - name: public
    - default: True
    - masquerade: False
    - ports:
      - 22/tcp
    - interfaces:
      - {{ mgmt_if }}
    - watch_in:
      - Start and enable Firewalld service

include:
  - .stop
