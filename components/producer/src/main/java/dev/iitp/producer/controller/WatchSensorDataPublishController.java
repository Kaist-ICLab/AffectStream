package dev.iitp.producer.controller;

import dev.iitp.producer.model.chest.SensorRecord;
import dev.iitp.producer.service.WatchSensorDataProducer;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

/**
 * Controller to handle incoming sensor data and publish it to a messaging topic.
 */
@Slf4j // Enable logging
@RestController // Mark this class as a REST controller handling HTTP requests
@RequiredArgsConstructor // Automatically injects dependencies via constructor
public class WatchSensorDataPublishController {

    @Value("${user.topic}") // Reads the topic name from the application properties
    private String TOPIC_NAME;
    private final WatchSensorDataProducer watchSensorDataProducer; // Kafka producer service

    /**
     * Handles HTTP POST requests to publish sensor data.
     *
     * @param chestSensorRecord The sensor data received in the request body.
     * @return "ok" if the request is processed successfully.
     */
    @PostMapping("/") // Handle POST requests to the root path
    public String publish(@RequestBody SensorRecord chestSensorRecord) {
        // Publish the sensor data to the Kafka topic asynchronously
        watchSensorDataProducer.async(TOPIC_NAME, chestSensorRecord);
        // Return success response
        return "ok";
    }
}
