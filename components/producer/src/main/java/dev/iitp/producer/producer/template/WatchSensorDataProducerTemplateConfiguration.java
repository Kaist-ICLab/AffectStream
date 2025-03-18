package dev.iitp.producer.producer.template;

import com.amazonaws.services.schemaregistry.serializers.GlueSchemaRegistryKafkaSerializer;
import com.amazonaws.services.schemaregistry.utils.AWSSchemaRegistryConstants;
import dev.iitp.producer.model.chest.SensorRecord;
import io.micrometer.core.instrument.MeterRegistry;
import io.micrometer.prometheus.PrometheusMeterRegistry;
import lombok.RequiredArgsConstructor;
import org.apache.kafka.clients.producer.ProducerConfig;
import org.apache.kafka.common.serialization.StringSerializer;
import org.springframework.boot.autoconfigure.kafka.KafkaProperties;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.kafka.core.DefaultKafkaProducerFactory;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.kafka.core.MicrometerProducerListener;
import org.springframework.kafka.core.ProducerFactory;
import software.amazon.awssdk.services.glue.model.DataFormat;
import org.apache.avro.generic.GenericRecord;

import java.util.Map;

/**
 * Kafka producer configuration for sending sensor data.
 * - Uses AWS Glue Schema Registry for message serialization.
 * - Configures Kafka producer properties and monitoring.
 */
@Configuration // Mark this class as a Spring configuration
@RequiredArgsConstructor // Automatically injects dependencies via constructor
public class WatchSensorDataProducerTemplateConfiguration {

    private final KafkaProperties properties; // Kafka properties

    /**
     * Creates a KafkaTemplate for producing sensor data messages.
     *
     * @param producerFactory The configured Kafka producer factory.
     * @return A KafkaTemplate instance for sending messages.
     */
    @Bean
    public KafkaTemplate<String, GenericRecord> watchSensorDataKafkaTemplate(ProducerFactory<String, GenericRecord> producerFactory) {
        return new KafkaTemplate<>(producerFactory);
    }

    /**
     * Creates a Kafka ProducerFactory with monitoring capabilities.
     *
     * @param meterRegistry Micrometer registry for metrics collection.
     * @param prometheusMeterRegistry Prometheus-specific registry for monitoring.
     * @return A configured ProducerFactory instance.
     */
    @Bean
    public ProducerFactory<String, GenericRecord> watchSensorDateProducerFactory(MeterRegistry meterRegistry,
                                                                                PrometheusMeterRegistry prometheusMeterRegistry) {
        Map<String, Object> props = watchSensorDataProducerConfig(); // Load producer configuration properties
        DefaultKafkaProducerFactory<String, GenericRecord> producerFactory = new DefaultKafkaProducerFactory<>(props); // Create a Kafka producer factory
        producerFactory.addListener(new MicrometerProducerListener<>(meterRegistry)); // Add a Micrometer listener for Kafka performance monitoring
        producerFactory.addListener(new MicrometerProducerListener<>(prometheusMeterRegistry));
        return producerFactory;
    }

    /**
     * Configures Kafka producer properties, including AWS Glue Schema Registry settings.
     *
     * @return A map of Kafka producer configurations.
     */
    private Map<String, Object> watchSensorDataProducerConfig() {
        // Set the AWS SDK HTTP service implementation to use URLConnection
        System.setProperty("software.amazon.awssdk.http.service.impl", "software.amazon.awssdk.http.urlconnection.UrlConnectionSdkHttpService");

        // Load default producer properties from Spring Boot Kafka properties
        Map<String, Object> props = this.properties.buildProducerProperties();

        props.put(ProducerConfig.ENABLE_IDEMPOTENCE_CONFIG, true); // Enable idempotent message delivery to avoid duplicate messages
        props.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class); // Configure key and value serializers
        // Configure AWS Glue Schema Registry settings
        props.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, GlueSchemaRegistryKafkaSerializer.class);
        props.put(AWSSchemaRegistryConstants.DATA_FORMAT, DataFormat.AVRO.name());
        props.put(AWSSchemaRegistryConstants.AWS_REGION, System.getenv("AWS_REGION")); // Set the AWS region
        props.put(AWSSchemaRegistryConstants.REGISTRY_NAME, System.getenv("AWS_SCHEMA_REGISTRY")); // Set the AWS Glue Schema Registry name
        props.put(AWSSchemaRegistryConstants.SCHEMA_NAME, System.getenv("AWS_GLUE_SCHEMA")); // Set the AWS Glue Schema name

        return props;
    }
}
