package dev.iitp.producer.service;

import com.fasterxml.jackson.databind.ObjectMapper;
import dev.iitp.producer.model.chest.SensorRecord;
import dev.iitp.producer.producer.callback.WatchSensorDataProducerCallback;
import lombok.extern.slf4j.Slf4j;
import org.apache.avro.generic.GenericDatumReader;
import org.apache.avro.generic.GenericRecord;
import org.apache.avro.Schema;
import org.apache.avro.io.DatumReader;
import org.apache.avro.io.DecoderFactory;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.kafka.support.SendResult;
import org.springframework.stereotype.Service;
import org.springframework.util.concurrent.ListenableFuture;

import java.io.IOException;
import java.io.InputStream;

/**
 * Service for producing Kafka messages with Avro serialization.
 * - Converts JSON messages to Avro format.
 * - Sends messages asynchronously to a Kafka topic.
 */
@Slf4j // Enable logging
@Service // Mark this class as a Spring service
public class WatchSensorDataProducer {

    private final WatchSensorDataProducerCallback watchSensorDataProducerCallback;
    private final KafkaTemplate<String, GenericRecord> watchSensorDataKafkaTemplate;
    private final Schema schema;
    // DatumReader instance methods are not thread-safe
    private final ThreadLocal<DatumReader<GenericRecord>> readerThreadLocal;

    /**
     * Constructor initializes the Avro schema and thread-local reader.
     *
     * @param callback      Callback handler for Kafka events.
     * @param kafkaTemplate KafkaTemplate for sending messages.
     */
    public WatchSensorDataProducer(WatchSensorDataProducerCallback callback, KafkaTemplate<String, GenericRecord> kafkaTemplate) {
        this.watchSensorDataProducerCallback = callback;
        this.watchSensorDataKafkaTemplate = kafkaTemplate;

        // Load the Avro schema from the resources directory
        try (InputStream is = this.getClass().getClassLoader().getResourceAsStream("SensorRecord.avsc")) {
            if (is != null) {
                this.schema = new Schema.Parser().parse(is);
            } else {
                throw new IOException("Schema file not found");
            }
        } catch (IOException e) {
            throw new RuntimeException("Error loading Avro schema", e);
        }

        // Initialize the ThreadLocal with a lambda that creates a new GenericDatumReader for each thread
        this.readerThreadLocal = ThreadLocal.withInitial(() -> new GenericDatumReader<>(this.schema));
    }

    /**
     * Converts a JSON string to an Avro GenericRecord.
     *
     * @param jsonString The JSON string representing sensor data.
     * @return The corresponding Avro GenericRecord.
     * @throws IOException If parsing fails.
     */
    private GenericRecord jsonToAvro(String jsonString) throws IOException {
        // Retrieve the thread-local DatumReader instance
        DatumReader<GenericRecord> reader = readerThreadLocal.get();

        // Deserialize the JSON string to a GenericRecord using the reader
        return reader.read(null, DecoderFactory.get().jsonDecoder(schema, jsonString));
    }

    /**
     * Asynchronously sends a sensor record to Kafka.
     *
     * @param topic   The Kafka topic to send the message to.
     * @param message The sensor data record.
     */
    public void async(String topic, SensorRecord message) {
        GenericRecord new_message;
        try {
            String jsonString = new ObjectMapper().writeValueAsString(message); // Convert the SensorRecord object to JSON string
            new_message = jsonToAvro(jsonString); // Convert JSON to Avro format
        } catch (IOException e) {
            e.printStackTrace();
            return;
        }
        if (new_message == null) return;
        
        // Send the Avro message asynchronously to Kafka
        ListenableFuture<SendResult<String, GenericRecord>> future = watchSensorDataKafkaTemplate.send(topic, message.getUserId(), new_message);
        future.addCallback(watchSensorDataProducerCallback); // Attach a callback to handle Kafka response
    }
}
