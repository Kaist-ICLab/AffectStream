package dev.iitp.publisher.model.wrist;

import lombok.Data;

import java.util.List;

@Data
public class ElectrodernalActivity {

    private int hz;
    private List<Double> value;
}
