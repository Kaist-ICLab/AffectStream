package dev.iitp.publisher.model.wrist;

import lombok.Data;

import java.util.List;

@Data
public class BloodVolumePressure {

    private int hz;
    private List<Double> value;
}
