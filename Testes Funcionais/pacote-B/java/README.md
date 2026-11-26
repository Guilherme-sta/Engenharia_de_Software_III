# Alternativa em Java
Os testes podem usar Java mesmo quando a aplicação testada usa Python.
Use JDK 17 ou 21 e Maven 3.9+. Inicie `python app.py` na raiz em outro terminal.
As versões do POM são referências fixadas, não uma afirmação de versões mais recentes.

Interface: `mvn test` (Chrome instalado, Selenium Manager pode precisar de internet).
Desempenho: `mvn gatling:test -Dgatling.simulationClass=ads.CatalogoSimulation`
O relatório fica em `target/gatling`. Não confunda os usuários simultâneos do
modelo fechado com chegadas por segundo do modelo aberto.
Para os patamares, altere users/duração na simulação, registre as alterações e
execute separadamente. Nos patamares de estresse, a falha das assertions pode
ser um resultado esperado e deve ser analisada.
As APIs usadas seguem a documentação oficial. Execute e registre as versões
no seu laboratório antes de adotá-las com a turma.
