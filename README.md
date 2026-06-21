# PROJETO INTEGRADOR I - CIVITAS

# Visão Geral
- O projeto consiste no desenvolvimento de uma plataforma dedicada à organização e transparência de dados do Poder Legislativo. O sistema monitora Projetos de Lei e o desempenho dos políticos envolvidos, visando reduzir as barreiras de acesso à informação e dar maior visibilidade às atividades parlamentares no Brasil.

# Metodologia e Ferramentas
- A ferramenta Figma foi utilizada para a concepção de todos os wireframes e fluxos de navegação. O design segue um padrão profissional com foco em usabilidade, utilizando uma paleta de cores institucional (predomínio de tons de azul e cinza) e componentes de interface modernos.

# Arquitetura de Telas e Fluxos
- O protótipo é composto por um fluxo de 7 telas principais interconectadas:

- Landing Page Educacional (/): Conteúdo focado em scrollytelling para explicar o sistema eleitoral e o processo legislativo brasileiro.

- Módulo de Autenticação (/auth): Interface de login e cadastro com integração para Google e Gov.br.

- Explorador de Leis (/explorer): Portal de busca de dados públicos com filtros avançados e visualização em grade de cards.

- Dashboard da Proposta (/dashboard): Painel de detalhes de um projeto de lei, incluindo:

- Gráfico de semicírculo (plenário) representando a votação.

- Linha do tempo da tramitação.

- Visualizador de documentos com comparação de versões (diff).

- Identificação de autor e relator.

- Perfil do Político (/politician/:id): Central de indicadores (KPIs), histórico de votações, gráficos de orçamento e grade de assiduidade.

- Páginas de Partidos e Comissões: Dashboards específicos para visualizar a agenda de comissões, membros e estatísticas partidárias.

# Implementações Técnicas de UX
- Navegação Integrada: O sistema permite navegar entre o dashboard de uma lei e o perfil de um parlamentar clicando diretamente nos assentos do plenário ou nos nomes de autores/relatores.
Visualização de Dados: Implementação de tooltips avançados no mapa do plenário, exibindo prévias de perfil (foto, partido e voto) ao passar o mouse.
Responsividade: Estrutura preparada para adaptação mobile, incluindo menus de navegação simplificados.

# Acesso ao Protótipo
- O wireframe completo e as interações podem ser visualizados através do link oficial do projeto.

- Link: [Legislative Tracking Dashboard](https://www.figma.com/make/0PxVMdAUDyXOsOsaXOG6LH/Legislative-Tracking-Dashboard?p=f&fullscreen=1)

- Senha de acesso: civitas

# Alunos Envolvidos
- [Lucas Borges](github.com/Borges070) - Pesquisador
- [Pedro Calderón](github.com/pedrocalderon52) - Pesquisador
- [Pedro Quartin](github.com/phquartin) - Pesquisador
- [Isaac Lovisi](github.com/IsaacLovisi) - Pesquisador
- [Artur Teles](github.com/arturjteles) - Pesquisador

- [Miguel Allievi](github.com/MIK2500) - Pesquisador
- [Heitor Vergueiro] - Consultor Jurídico
