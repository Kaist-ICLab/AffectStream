package dev.iitp.publisher.model.wrist;

import com.fasterxml.jackson.databind.PropertyNamingStrategies;
import com.fasterxml.jackson.databind.annotation.JsonNaming;
import lombok.Data;


@Data
@JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy.class)
public class SensorRecord {

    private String userId;
    private long timestamp;
    private Value value;

    @Data
    static class Value {
        private Accelerometer acc;
        private BloodVolumePressure bvp;
        private ElectrodernalActivity eda;
        private HeartRate hr;
        private Temperature temp;
    }
}
