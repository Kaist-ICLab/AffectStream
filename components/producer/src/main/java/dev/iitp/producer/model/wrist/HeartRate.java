package dev.iitp.producer.model.wrist;

import lombok.Data;

import java.util.List;

@Data
public class HeartRate {

    private int hz;
    private List<Double> value;
}
