-- ============================================================
-- SEED DE MATERIA 
-- 60 registros
--
-- STATUS:
-- 0 = EM_ANDAMENTO
-- 1 = APROVADA
-- 2 = REPROVADA
-- ============================================================

INSERT INTO materia
(titulo, subtitulo, resumo, conteudo, data, status, id_setor, cpf_editor_chefe)
VALUES

('Avanço da Inteligência Artificial nos Setores de Serviços',
 'Uma análise sobre o crescimento da inteligência artificial.'
 'Estudo sobre os impactos da inteligência artificial nos serviços.',
 'A expansão da inteligência artificial vem modificando processos e serviços em diferentes setores da sociedade.',
 '2026-01-05', 0, 1, '00000000001'),

('Novas Políticas Econômicas e o Impacto na Inflação',
 'Mudanças econômicas e seus efeitos.',
 'Análise das novas políticas econômicas e seus impactos.',
 'As mudanças nas políticas econômicas podem influenciar diretamente a inflação e o comportamento dos consumidores.',
 '2026-01-07', 1, 2, '00000000002'),

('Reforma Tributária: O Que Muda para o Consumidor',
 'Principais mudanças previstas.',
 'Entenda os efeitos da reforma tributária.',
 'A reforma tributária apresenta mudanças que podem afetar consumidores e empresas em diferentes setores.',
 '2026-01-09', 2, 3, '00000000003'),

('Grandes Obras de Infraestrutura no País',
 'Investimentos em infraestrutura.',
 'Panorama das principais obras de infraestrutura.',
 'Grandes projetos de infraestrutura podem contribuir para o desenvolvimento econômico e social.',
 '2026-01-11', 0, 4, '00000000004'),

('A Crise Climática e o Futuro das Cidades',
 'Desafios ambientais urbanos.',
 'Os impactos das mudanças climáticas nas cidades.',
 'O crescimento urbano exige novas estratégias para enfrentar eventos climáticos e reduzir impactos ambientais.',
 '2026-01-13', 1, 5, '00000000005'),

('Descobertas Recentes na Exploração Espacial',
 'Novos avanços científicos.',
 'Descobertas recentes no setor espacial.',
 'Novas pesquisas espaciais ampliam o conhecimento científico sobre o universo e seus fenômenos.',
 '2026-01-15', 2, 6, '00000000006'),

('O Crescimento do Mercado de Veículos Elétricos',
 'Transformações no setor automotivo.',
 'Análise do mercado de veículos elétricos.',
 'O mercado de veículos elétricos apresenta crescimento impulsionado por novas tecnologias e mudanças ambientais.',
 '2026-01-17', 0, 7, '00000000007'),

('Desafios do Sistema de Saúde Pública',
 'Questões enfrentadas pelo setor.',
 'Análise dos principais desafios da saúde pública.',
 'O sistema de saúde pública enfrenta desafios relacionados à demanda, infraestrutura e distribuição de recursos.',
 '2026-01-19', 1, 8, '00000000008'),

('A Evolução da Educação Digital no Brasil',
 'Tecnologia aplicada ao ensino.',
 'O crescimento das ferramentas digitais na educação.',
 'A educação digital vem ampliando as possibilidades de acesso ao conhecimento e às ferramentas de aprendizagem.',
 '2026-01-21', 2, 9, '00000000009'),

('Tendências no Mercado Financeiro Internacional',
 'Mudanças no cenário financeiro.',
 'Principais tendências do mercado internacional.',
 'O mercado financeiro internacional passa por transformações influenciadas por tecnologia e políticas econômicas.',
 '2026-01-23', 0, 10, '00000000010'),

('Expansão das Energias Renováveis',
 'Novas fontes de energia.',
 'Crescimento das energias renováveis.',
 'Investimentos em energias renováveis aumentam a participação de fontes alternativas na matriz energética.',
 '2026-01-25', 1, 1, '00000000001'),

('Tecnologia e Transformação do Mercado de Trabalho',
 'Mudanças nas profissões.',
 'Como a tecnologia altera o mercado de trabalho.',
 'Novas tecnologias estão transformando profissões, processos produtivos e formas de organização do trabalho.',
 '2026-01-27', 2, 2, '00000000002'),

('Segurança Digital e Proteção de Dados',
 'Desafios da segurança da informação.',
 'A importância da proteção de dados.',
 'A segurança digital tornou-se essencial para organizações que trabalham diariamente com informações.',
 '2026-01-29', 0, 3, '00000000003'),

('Crescimento das Cidades Inteligentes',
 'Tecnologia aplicada às cidades.',
 'O conceito de cidades inteligentes.',
 'Soluções tecnológicas podem melhorar serviços públicos, mobilidade urbana e qualidade de vida.',
 '2026-01-31', 1, 4, '00000000004'),

('Novos Caminhos para a Mobilidade Urbana',
 'Alternativas para o transporte.',
 'Desafios da mobilidade nas grandes cidades.',
 'A mobilidade urbana exige planejamento e investimentos em diferentes formas de transporte.',
 '2026-02-02', 2, 5, '00000000005'),

('A Importância da Ciência para a Sociedade',
 'Pesquisa e desenvolvimento científico.',
 'O papel da ciência no desenvolvimento.',
 'A pesquisa científica contribui para avanços tecnológicos, sociais e econômicos.',
 '2026-02-04', 0, 6, '00000000006'),

('Mudanças no Comportamento do Consumidor',
 'Novos hábitos de consumo.',
 'Transformações nos hábitos dos consumidores.',
 'Tecnologia e mudanças sociais influenciam diretamente as decisões e os hábitos de consumo.',
 '2026-02-06', 1, 7, '00000000007'),

('O Papel das Startups na Economia',
 'Empreendedorismo e inovação.',
 'A contribuição das startups para a economia.',
 'Startups podem estimular inovação e criar novos modelos de negócios em diferentes segmentos.',
 '2026-02-08', 2, 8, '00000000008'),

('Avanços Recentes na Medicina',
 'Tecnologia aplicada à saúde.',
 'Novas tecnologias médicas.',
 'Novos métodos e tecnologias estão contribuindo para diagnósticos e tratamentos mais eficientes.',
 '2026-02-10', 0, 9, '00000000009'),

('Internet das Coisas e Vida Cotidiana',
 'Dispositivos conectados.',
 'O crescimento da Internet das Coisas.',
 'Dispositivos conectados estão sendo utilizados em residências, empresas e serviços públicos.',
 '2026-02-12', 1, 10, '00000000010'),

('Desenvolvimento da Computação em Nuvem',
 'Serviços digitais na nuvem.',
 'A expansão da computação em nuvem.',
 'A computação em nuvem permite acesso flexível a recursos computacionais e serviços digitais.',
 '2026-02-14', 2, 1, '00000000001'),

('Novas Tecnologias de Comunicação',
 'Transformações na comunicação.',
 'Tecnologias que mudaram a comunicação.',
 'Novas plataformas digitais modificaram a maneira como pessoas e organizações se comunicam.',
 '2026-02-16', 0, 2, '00000000002'),

('O Crescimento do Comércio Eletrônico',
 'Expansão das compras online.',
 'Panorama do comércio eletrônico.',
 'O comércio eletrônico vem ampliando as opções de compra e venda de produtos e serviços.',
 '2026-02-18', 1, 3, '00000000003'),

('Desafios da Segurança Alimentar',
 'Produção e distribuição de alimentos.',
 'Questões relacionadas à segurança alimentar.',
 'A segurança alimentar depende de políticas eficientes de produção, distribuição e acesso aos alimentos.',
 '2026-02-20', 2, 4, '00000000004'),

('Turismo e Desenvolvimento Regional',
 'Impactos econômicos do turismo.',
 'O turismo como instrumento de desenvolvimento.',
 'O turismo pode contribuir para geração de empregos e desenvolvimento econômico de diferentes regiões.',
 '2026-02-22', 0, 5, '00000000005'),

('Preservação das Florestas Brasileiras',
 'Proteção ambiental.',
 'Desafios da preservação florestal.',
 'A preservação das florestas é fundamental para a biodiversidade e o equilíbrio ambiental.',
 '2026-02-24', 1, 6, '00000000006'),

('Novas Estratégias para a Agricultura',
 'Tecnologia no campo.',
 'Inovação no setor agrícola.',
 'Tecnologias agrícolas podem aumentar a produtividade e melhorar o uso dos recursos naturais.',
 '2026-02-26', 2, 7, '00000000007'),

('O Futuro das Telecomunicações',
 'Evolução das redes de comunicação.',
 'Novas tendências das telecomunicações.',
 'A evolução das redes permite conexões mais rápidas e amplia o acesso aos serviços digitais.',
 '2026-02-28', 0, 8, '00000000008'),

('Inteligência Artificial na Educação',
 'Aplicações educacionais da IA.',
 'Uso da inteligência artificial no ensino.',
 'Ferramentas de inteligência artificial podem auxiliar professores e estudantes em diferentes atividades.',
 '2026-03-02', 1, 9, '00000000009'),

('Transformações no Jornalismo Digital',
 'Mudanças na produção de notícias.',
 'O jornalismo diante das novas tecnologias.',
 'As plataformas digitais modificaram a produção, distribuição e consumo de notícias.',
 '2026-03-04', 2, 10, '00000000010'),

('Novos Modelos de Negócios Digitais',
 'Inovação empresarial.',
 'Modelos de negócios baseados em tecnologia.',
 'A transformação digital possibilitou o surgimento de novos modelos de negócios.',
 '2026-03-06', 0, 1, '00000000001'),

('A Expansão dos Serviços de Streaming',
 'Mudanças no consumo de conteúdo.',
 'Crescimento das plataformas de streaming.',
 'Os serviços de streaming transformaram o acesso a filmes, séries, músicas e outros conteúdos.',
 '2026-03-08', 1, 2, '00000000002'),

('Tecnologia e Preservação Cultural',
 'Digitalização do patrimônio.',
 'Tecnologia aplicada à cultura.',
 'Ferramentas digitais podem contribuir para preservação e divulgação do patrimônio cultural.',
 '2026-03-10', 2, 3, '00000000003'),

('O Futuro da Automação Industrial',
 'Indústria e tecnologia.',
 'Avanços da automação industrial.',
 'A automação industrial permite maior eficiência e precisão em diferentes processos produtivos.',
 '2026-03-12', 0, 4, '00000000004'),

('Novas Perspectivas para a Pesquisa Científica',
 'Ciência e inovação.',
 'Perspectivas para a pesquisa científica.',
 'Novas ferramentas tecnológicas estão ampliando as possibilidades da pesquisa científica.',
 '2026-03-14', 1, 5, '00000000005'),

('A Importância da Inclusão Digital',
 'Acesso à tecnologia.',
 'Desafios da inclusão digital.',
 'A inclusão digital é importante para ampliar o acesso da população a serviços e oportunidades.',
 '2026-03-16', 2, 6, '00000000006'),

('Transformações no Setor Bancário',
 'Digitalização dos bancos.',
 'Mudanças nos serviços bancários.',
 'A digitalização vem transformando a forma como clientes utilizam serviços financeiros.',
 '2026-03-18', 0, 7, '00000000007'),

('O Crescimento das Fintechs',
 'Tecnologia e finanças.',
 'Expansão das empresas financeiras digitais.',
 'As fintechs oferecem novos serviços e soluções para o mercado financeiro.',
 '2026-03-20', 1, 8, '00000000008'),

('Novos Desafios da Privacidade Digital',
 'Proteção das informações pessoais.',
 'Privacidade no ambiente digital.',
 'A expansão dos serviços digitais aumenta a importância da proteção das informações pessoais.',
 '2026-03-22', 2, 9, '00000000009'),

('Tecnologia Aplicada ao Meio Ambiente',
 'Soluções tecnológicas ambientais.',
 'Tecnologia e sustentabilidade.',
 'Soluções tecnológicas podem auxiliar no monitoramento e na preservação ambiental.',
 '2026-03-24', 0, 10, '00000000010'),

('O Papel das Universidades na Inovação',
 'Pesquisa acadêmica e tecnologia.',
 'Universidades e desenvolvimento tecnológico.',
 'Universidades possuem papel relevante na formação de profissionais e no desenvolvimento científico.',
 '2026-03-26', 1, 1, '00000000001'),

('Mudanças na Indústria de Entretenimento',
 'Novos formatos de conteúdo.',
 'Transformações no entretenimento.',
 'A tecnologia modificou a produção e o consumo de conteúdos de entretenimento.',
 '2026-03-28', 2, 2, '00000000002'),

('Desafios da Infraestrutura Digital',
 'Expansão da conectividade.',
 'Infraestrutura necessária para serviços digitais.',
 'A expansão da conectividade depende de investimentos em infraestrutura digital.',
 '2026-03-30', 0, 3, '00000000003'),

('O Futuro dos Transportes Autônomos',
 'Tecnologia e mobilidade.',
 'Avanços nos transportes autônomos.',
 'Novas tecnologias estão sendo desenvolvidas para automatizar diferentes formas de transporte.',
 '2026-04-01', 1, 4, '00000000004'),

('Novas Tecnologias de Armazenamento de Energia',
 'Inovação no setor energético.',
 'Avanços no armazenamento de energia.',
 'Novas tecnologias de armazenamento podem contribuir para a expansão das fontes renováveis.',
 '2026-04-03', 2, 5, '00000000005'),

('O Impacto das Redes Sociais na Comunicação',
 'Comunicação na era digital.',
 'Redes sociais e comunicação.',
 'As redes sociais alteraram significativamente a forma de produção e distribuição de informações.',
 '2026-04-05', 0, 6, '00000000006'),

('Desenvolvimento de Tecnologias Sustentáveis',
 'Inovação e sustentabilidade.',
 'Tecnologias voltadas à sustentabilidade.',
 'Novas soluções tecnológicas buscam reduzir impactos ambientais e melhorar a eficiência dos recursos.',
 '2026-04-07', 1, 7, '00000000007'),

('A Evolução dos Sistemas de Informação',
 'Tecnologia nas organizações.',
 'Transformações nos sistemas de informação.',
 'Sistemas de informação são fundamentais para gerenciamento e análise de dados nas organizações.',
 '2026-04-09', 2, 8, '00000000008'),

('O Crescimento da Economia Digital',
 'Novos mercados e tecnologias.',
 'Expansão da economia digital.',
 'A economia digital vem criando novas oportunidades para empresas e consumidores.',
 '2026-04-11', 0, 9, '00000000009'),

('Novas Soluções para a Mobilidade Sustentável',
 'Transporte e sustentabilidade.',
 'Alternativas sustentáveis para mobilidade.',
 'Soluções sustentáveis podem reduzir impactos ambientais relacionados ao transporte urbano.',
 '2026-04-13', 1, 10, '00000000010'),

('Tecnologia e Gestão Pública',
 'Inovação nos serviços públicos.',
 'Tecnologia aplicada à administração pública.',
 'Ferramentas digitais podem melhorar a eficiência e a transparência dos serviços públicos.',
 '2026-04-15', 2, 1, '00000000001'),

('Desafios da Transformação Digital',
 'Mudanças organizacionais.',
 'Desafios enfrentados pelas organizações.',
 'A transformação digital exige adaptação de processos, pessoas e estratégias organizacionais.',
 '2026-04-17', 0, 2, '00000000002'),

('Novas Perspectivas para o Mercado de Trabalho',
 'Profissões e tecnologia.',
 'Mudanças nas relações de trabalho.',
 'As transformações tecnológicas estão criando novas oportunidades e desafios profissionais.',
 '2026-04-19', 1, 3, '00000000003'),

('A Importância da Inovação Tecnológica',
 'Tecnologia e competitividade.',
 'Inovação como fator de desenvolvimento.',
 'A inovação tecnológica pode aumentar a competitividade e melhorar produtos e serviços.',
 '2026-04-21', 2, 4, '00000000004'),

('O Papel dos Dados na Tomada de Decisões',
 'Dados e gestão.',
 'Uso estratégico dos dados.',
 'A análise de dados permite identificar padrões e apoiar processos de tomada de decisão.',
 '2026-04-23', 0, 5, '00000000005'),

('Desenvolvimento de Novas Tecnologias Médicas',
 'Inovação na saúde.',
 'Tecnologias aplicadas à medicina.',
 'O desenvolvimento tecnológico vem ampliando as possibilidades de diagnóstico e tratamento.',
 '2026-04-25', 1, 6, '00000000006'),

('O Futuro da Conectividade Global',
 'Redes e comunicação.',
 'Expansão da conectividade mundial.',
 'Novas tecnologias de comunicação podem ampliar o acesso à internet em diferentes regiões.',
 '2026-04-27', 2, 7, '00000000007'),

('Tecnologia e Desenvolvimento Econômico',
 'Inovação e economia.',
 'Relação entre tecnologia e desenvolvimento.',
 'O desenvolvimento tecnológico pode contribuir para produtividade, inovação e crescimento econômico.',
 '2026-04-29', 0, 8, '00000000008'),

('Novas Tendências em Tecnologia da Informação',
 'Inovações no setor de TI.',
 'Principais tendências tecnológicas.',
 'Novas tendências em tecnologia da informação continuam transformando organizações e serviços.',
 '2026-05-01', 1, 9, '00000000009'),

('Desafios da Sociedade Conectada',
 'Tecnologia e sociedade.',
 'Impactos da conectividade.',
 'A sociedade conectada apresenta novas oportunidades, mas também exige atenção a segurança e privacidade.',
 '2026-05-03', 2, 10, '00000000010'),

('O Futuro da Inteligência Artificial',
 'Perspectivas para a IA.',
 'Novos caminhos para a inteligência artificial.',
 'O avanço da inteligência artificial abre novas possibilidades de aplicação em diferentes áreas.',
 '2026-05-05', 0, 1, '00000000001'),

('Tecnologia e Mudanças Sociais',
 'Impactos sociais da tecnologia.',
 'Tecnologia e transformação social.',
 'As novas tecnologias influenciam comportamentos, relações sociais e formas de acesso à informação.',
 '2026-05-07', 1, 2, '00000000002'),

('Inovação e Competitividade Empresarial',
 'Empresas e inovação.',
 'A inovação como estratégia empresarial.',
 'Empresas que investem em inovação podem desenvolver novos produtos, serviços e processos.',
 '2026-05-09', 2, 3, '00000000003'),

('Novas Estratégias para o Desenvolvimento Sustentável',
 'Sustentabilidade e inovação.',
 'Estratégias para desenvolvimento sustentável.',
 'O desenvolvimento sustentável depende da integração entre crescimento econômico, preservação ambiental e bem-estar social.',
 '2026-05-11', 0, 4, '00000000004'),

('O Impacto da Tecnologia na Educação',
 'Educação e inovação.',
 'Tecnologia no processo educacional.',
 'A tecnologia pode ampliar recursos educacionais e oferecer novas formas de aprendizagem.',
 '2026-05-13', 1, 5, '00000000005'),

('Novos Caminhos para a Ciência e Tecnologia',
 'Pesquisa e inovação.',
 'Perspectivas para ciência e tecnologia.',
 'A integração entre ciência e tecnologia pode gerar soluções para diferentes desafios da sociedade.',
 '2026-05-15', 2, 6, '00000000006'),

('Transformações Digitais nas Organizações',
 'Empresas na era digital.',
 'Digitalização dos processos organizacionais.',
 'A digitalização dos processos pode melhorar a eficiência e facilitar o gerenciamento das organizações.',
 '2026-05-17', 0, 7, '00000000007'),

('O Crescimento das Soluções Baseadas em Dados',
 'Dados e tecnologia.',
 'Soluções orientadas por dados.',
 'O uso estratégico de dados permite desenvolver soluções mais eficientes para diferentes setores.',
 '2026-05-19', 1, 8, '00000000008'),

('Perspectivas para o Futuro da Tecnologia',
 'Tecnologia e inovação.',
 'Reflexões sobre o futuro tecnológico.',
 'O desenvolvimento tecnológico continuará influenciando diferentes áreas da sociedade e da economia.',
 '2026-05-21', 2, 9, '00000000009'),

('Tecnologia e Novas Formas de Comunicação',
 'Comunicação digital.',
 'Novas formas de interação.',
 'As tecnologias digitais continuam criando novas formas de comunicação e compartilhamento de informações.',
 '2026-05-23', 0, 10, '00000000010')

ON CONFLICT DO NOTHING;