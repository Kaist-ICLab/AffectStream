package dev.iitp.producer.model.chest;

import lombok.Data;

import java.util.List;

@Data
public class Respiration {

    private int hz;
    private List<Integer> value;
}
