package ads;
import io.gatling.javaapi.core.*;
import io.gatling.javaapi.http.*;
import static io.gatling.javaapi.core.CoreDsl.*;
import static io.gatling.javaapi.http.HttpDsl.*;
import java.time.Duration;

public class CatalogoSimulation extends Simulation {
    HttpProtocolBuilder protocolo = http.baseUrl("http://127.0.0.1:8000");
    ScenarioBuilder leitor = scenario("Catalogo").during(Duration.ofSeconds(90)).on(
        exec(http("catalogo").get("/api/livros?q=software")
        .check(status().is(200), jsonPath("$.total").ofInt().gt(0),
               jsonPath("$.itens[0].id").exists()))
        .pause(Duration.ofMillis(200), Duration.ofMillis(600))
    );
    { setUp(leitor.injectClosed(constantConcurrentUsers(20).during(Duration.ofSeconds(90))))
        .protocols(protocolo).maxDuration(Duration.ofSeconds(90))
        .assertions(global().responseTime().percentile(95.0).lte(500),
                    global().failedRequests().percent().lte(1.0)); }
}
