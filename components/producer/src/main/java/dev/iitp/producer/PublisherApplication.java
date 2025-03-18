package dev.iitp.producer;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

/**
 * Entry point for the producer Spring Boot application.
 * 
 * - This class initializes and runs the Spring Boot application.
 * - Uses `@SpringBootApplication` to enable auto-configuration and component scanning.
 */
@SpringBootApplication // Enable Spring Boot auto-configuration and component scanning
public class producerApplication {

	/**
     * Main method to launch the Spring Boot application.
     *
     * @param args Command-line arguments.
     */
	public static void main(String[] args) {
		SpringApplication.run(producerApplication.class, args);
	}

}
