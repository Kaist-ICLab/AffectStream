package dev.iitp.publisher.model.wrist;

import lombok.Data;

import java.util.List;

@Data
public class Accelerometer {

    private int hz;
    private List<Axis> value;
}
