package dev.iitp.publisher.model.chest;

import com.fasterxml.jackson.databind.PropertyNamingStrategies;
import com.fasterxml.jackson.databind.annotation.JsonNaming;
import lombok.Data;

import java.util.List;

@Data
@JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy.class)
public class SensorRecord {

    private String userId;
    private String connectionId;
    private long timestamp;
    private int segmentSize;
    private Value value;

    @Data
    @JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy.class)
    static class Value {
        private Accelerometer chestAcc;
        private Electrocardiogram chestEcg;
        private ElectrodernalActivity chestEda;
        private Electromyogram chestEmg;
        private Temperature chestTemp;
        private Respiration chestResp;
    }
}
