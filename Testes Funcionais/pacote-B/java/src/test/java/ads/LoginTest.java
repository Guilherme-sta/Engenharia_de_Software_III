package ads;
import java.time.Duration;
import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;
import org.openqa.selenium.*;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.support.ui.*;

class LoginTest {
    WebDriver driver;
    @BeforeEach void iniciar() { driver = new ChromeDriver(); }
    @AfterEach void encerrar() { if (driver != null) driver.quit(); }
    void preencher(String senha) {
        driver.get("http://127.0.0.1:8000/login");
        driver.findElement(By.id("email")).sendKeys("aluno@ads.local");
        driver.findElement(By.id("senha")).sendKeys(senha);
        driver.findElement(By.id("entrar")).click();
    }
    @Test void loginValido() {
        preencher("Teste123!");
        WebElement titulo = new WebDriverWait(driver, Duration.ofSeconds(5)).until(
            ExpectedConditions.visibilityOfElementLocated(By.id("boas-vindas")));
        assertEquals("Bem-vindo, Aluno ADS", titulo.getText());
        assertTrue(driver.getCurrentUrl().endsWith("/painel"));
    }
    @Test void loginInvalido() {
        preencher("senha-errada");
        new WebDriverWait(driver, Duration.ofSeconds(5)).until(
            ExpectedConditions.textToBePresentInElementLocated(By.id("erro"), "Credenciais inválidas"));
        assertTrue(driver.getCurrentUrl().endsWith("/login"));
        assertTrue(driver.findElements(By.id("boas-vindas")).isEmpty());
    }
}
