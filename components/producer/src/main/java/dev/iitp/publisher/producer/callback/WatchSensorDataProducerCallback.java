package dev.iitp.publisher.producer.callback;

import dev.iitp.publisher.model.chest.SensorRecord;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.kafka.core.KafkaProducerException;
import org.springframework.kafka.core.KafkaSendCallback;
import org.springframework.kafka.support.SendResult;
import org.springframework.stereotype.Component;
import org.apache.avro.generic.GenericRecord;

import java.time.Instant;
import java.time.LocalDateTime;

/**
 * Callback handler for Kafka producer events.
 * - Handles success and failure scenarios when sending sensor data.
 */
@Slf4j // Enable logging
@Component // Mark this class as a Spring component
@RequiredArgsConstructor // Automatically injects dependencies via constructor
public class WatchSensorDataProducerCallback implements KafkaSendCallback<String, GenericRecord> {

    @Value("${user.nodeId}") // Reads the node ID from the application properties
    private int nodeId;

    /**
     * Handles failure scenarios when Kafka message sending fails.
     *
     * @param ex The exception thrown by Kafka producer.
     */
    @Override
    public void onFailure(KafkaProducerException ex) {
        log.error("Produce failed", ex);
    }

    /**
     * Handles success scenarios when Kafka message sending succeeds.
     *
     * @param result The result of the Kafka send operation.
     */
    @Override
    public void onSuccess(SendResult<String, GenericRecord> result) {
        GenericRecord sensorRecord = result.getProducerRecord().value(); // Retrieve the sensor record
        long timestamp = Instant.now().toEpochMilli(); // Get the current timestamp in milliseconds
        log.info("[Success] user id: {}, created at: {}, latency: {}", 
            sensorRecord.get("user_id"), 
            sensorRecord.get("timestamp"), 
            timestamp - Long.parseLong(String.valueOf(sensorRecord.get("timestamp")))
        );
    }