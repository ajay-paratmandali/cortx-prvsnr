Create Certs user:
  user.present:
    - name: certs
    - createhome: False
    - shell: /sbin/nologin

Create s3 certs directory:
  file.directory:
    - names:
      - /etc/ssl/stx-s3/s3
      - /etc/ssl/stx-s3/s3auth
    - makedirs: True
    - dir_mode: 755
    - file_mode: 644
    - user: certs
    - group: certs
    - recurse:
      - user
      - group
      - mode
    - require:
      - user: Create Certs user


{% if pillar["cluster"][grains["id"]]["is_primary"] %}
Untar the Tar files:
  archive.extracted:
    - name: /opt/seagate/certs/
    - source: /opt/seagate/tar_file.tar
    - enforce_toplevel: False
    - keep_source: True
    - clean: False
    - trim_output: True

{%- for node_id in pillar['cluster']['node_list'] -%}
{%- if not pillar['cluster'][node_id]['is_primary'] %}

Copy certs to non-primary:
  cmd.run:
    - name: scp -r /opt/seagate/certs {{ pillar['cluster'][node_id]['hostname'] }}:/opt/seagate/

{%- endif -%}
{%- endfor -%}
{% endif %}


Copy certs to s3 and s3auth directories:
  file.recurse:
    - names:
      - /etc/ssl/stx-s3/s3
      - /etc/ssl/stx-s3/s3auth
    - source: /opt/seagate/certs/*
    - keep_source: False
    - clean: False
    - user: certs
    - group certs 
    - dir_mode: 755
    - file_mode: 644

Clean certs:
  file.absent:
    - name: /opt/seagate/certs

#Add haproxy user:
#  module.run:
#    - groupadd.adduser: 
#      - name: certs
#      - user: haproxy
