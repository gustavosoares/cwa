
##########################################
1. Criacao de usuario no banco de dados:
##########################################

grant all on monitor to monitor@localhost;
GRANT ALL ON monitor.* TO monitor@'%' IDENTIFIED BY 'monitor';
GRANT ALL ON monitor.* TO monitor@localhost IDENTIFIED BY 'monitor';

##########################################
2. Dump dos dados em json
##########################################

python2.5 manage.py dumpdata --indent 2 --exclude=sites --exclude=admin --exclude=sessions --exclude=contenttypes --exclude=sme

##############################################
3. Carregar dados iniciais para a aplicacao
##############################################

python2.5 manage.py loaddata modelo/fixtures/initial_data.json

##############################################
4. Gerar o xml
##############################################

http://localhost:8000/relatorio/xml?produto=35&alarme=125&monitor=396&data_inicio=2009-07-01&data_fim=2009-10-31


TIPS

Install Django Command Extensions (http://code.google.com/p/django-command-extensions) 
and pygraphviz (http://networkx.lanl.gov/pygraphviz/) and then issue the following command to get a really nice looking Django model visualization:

./manage.py graph_models -a -g -o my_project.png

Here's an example output from the Django Command Extensions page.

########################################
5. Gerando a entidade relacional
########################################

python modelviz.py sme > sme.dot
/opt/local/bin/dot sme.dot -Tpng -o sme.png

python modelviz.py modelo > modelo.dot
/opt/local/bin/dot modelo.dot -Tpng -o modelo.png

########################################
6. Alterando a tabela
########################################

 alter table modelo_widget add column url_ajuda varchar(100);

NOT NULL

BEGIN;
ALTER TABLE modelo_modelo ADD COLUMN template_id integer;
UPDATE modelo_modelo SET template_id=0;
ALTER TABLE modelo_modelo ALTER COLUMN template_id SET NOT NULL;
COMMIT;