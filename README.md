# Avaliação de conhecimentos em Desenvolvimento de Software

Site no ar: https://pw-sharer.herokuapp.com/
(Dados de acesso serão enviados por e-mail)

## Design

### Backend:
- Django
- PostgreSQL

As principais funções desenvolvidas no backend se encontram nos seguintes caminhos:
- apps/security_app/views.py
- apps/security_app/validation

A criação dos modelos a serem importados para o banco de dados pode ser encontrada em:
- apps/security_app/models.py

### Frontend:
- Javascript
- Bootstrap 
- Templates (montados no servidor e renderizados no frontend)

As funções desenvolvidas para o frontend (especialmente a função de geração de senha) se encontram em:
- pw_sharer/static/js/scripts.js

Outros arquivos estáticos: pw_sharer/static

Templates: pw_sharer/templates

### Nuvem/Deploy:
- Heroku (deploy contínuo com github)

---

### Controles de segurança


Para facilitar a visualização e os testes do funcionamento do projeto, foram implementadas algumas telas adicionais como: 
- Login;
- Logged, que aparece quando um usuário não admnistrador faz login;
- Dashboard, que contém todos os links gerados e seus respectivos status

Também foi desenvolvida uma tela que mostra o link (display_link), de forma que o adminstrador consiga compartilhar a senha sem precisar entrar no link.

Para esse desafio não foi desenvolvida uma tela de cadastramento de novos usuários, mas caso haja necessidade é possível criá-los através do painel admin (https://pw-sharer.herokuapp.com/admin)

O framework Django possui várias funcionalidades nativas de segurança que foram utilizadas nesse projeto, tais como a parte de autenticação de usuários, CSRF token e hash de senhas. 

Uma das medidas de segurança adotadas foi definir quais visualizações eram restritas ao administrador,  quais eram acessíveis por usuários comuns e quais eram públicas. Para isso, os métodos de autenticação do Django e os atributos de usuário foram utilizados para validação de cada caso (veja detahes em apps/security_app/views.py).

Por não ser possível recuperar as senhas diretamente do usuário (justamente por estarem encriptografadas), foi necessário armazenar a senha na base de dados dos links de compartilhamento (sharers) de forma porvisória. Em todas as views em que os shares sejam chamados, em especial no sharer em si, é feita uma validação sobre o seu status. Caso o sharer não esteja mais disponível (pelo limite de acessos ou pela data), a senha é apagada daquele sharer e seu status é atualizado, impedindo a visualização.

Outra medida de segurança utilizada foi o uso de variáveis de ambiente do heroku para subir a aplicação em produção, relativamente aos dados de acesso ao banco de dados e ao servidor Django.

A geração aleatória de senhas, por não utilizar informações sigilosas e por uma questão de agilidade na visualização, foi desenvolvida utilizando Javascript no frontend. São utilizados letras minúsculas, maiúsculas, números e caracteres especiais, com um comprimento padrão de 16 caracteres, embaralhados de forma aleatória, cuja regra é que haja pelo menos um caracter de cada tipo. É sorteado o comprimento de cada tipo de string, cuja soma com o comprimento de outras strings seja equivalente ao compimento definido como argumento da função. (veja detalhes em pw_sharer/static/js/scripts.js)

Já a validação da nova senha criada ao gerar o link é realizada no backend, dentro de apps/security_app/validation/validation.py. A senha deve ter pelo menos 8 digitos e pelo menos um caracter de cada tipo para ser aceita. Caso não haja algum desses requisitos, retorna uma mensagem de erro.






