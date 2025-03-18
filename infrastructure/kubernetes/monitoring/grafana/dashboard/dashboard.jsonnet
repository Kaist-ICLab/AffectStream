local grafana = import 'grafonnet/grafana.libsonnet';
local dashboard = grafana.dashboard;
local prometheus = grafana.prometheus;
local template = grafana.template;

local textPanel = grafana.text;
local graphPanel = grafana.graphPanel;

dashboard.new(
  title='Kafka Producer Metrics',
  editable=true,
  time_from='now-15m',
  refresh='30s',
)
.addPanels([
  //################ Row ##################
  textPanel.new(
    mode='html',
    content='<h2><center>Buffer 구간</center></h2>',
  ) + { gridPos: { h: 2, w: 24, x: 0, y: 0 } },
  //################ Row ##################
  graphPanel.new(
    title='Compression Rate',
    description='프로듀서 레코드 압축률',
    fill=1,
    datasource=prometheus,
  )
  .addTargets([
    prometheus.target(
      expr='kafka_producer_compression_rate_avg',
      intervalFactor=1,
      legendFormat='{{instance}}'
    ),
  ]) + { gridPos: { h: 8, w: 8, x: 0, y: 2 } },
  graphPanel.new(
    title='Waiting Threads',
    description='대기 중인 쓰레드',
    fill=1,
    datasource=prometheus,
  )
  .addTargets([
    prometheus.target(
      expr='kafka_producer_waiting_threads',
      intervalFactor=1,
      legendFormat='{{instance}}'
    ),
  ]) + { gridPos: { h: 8, w: 8, x: 8, y: 2 } },
  graphPanel.new(
    title='Buffer Available Size(bytes)',
    description='가용한 버퍼 사이즈',
    fill=1,
    datasource=prometheus,
  )
  .addTargets([
    prometheus.target(
      expr='kafka_producer_buffer_available_bytes',
      intervalFactor=1,
      legendFormat='{{instance}}'
    ),
  ]) + { gridPos: { h: 8, w: 8, x: 16, y: 2 } },
  //################ Row ##################
  graphPanel.new(
    title='Bufferpool Wait Ratio',
    description='Buffer pool에 데이터를 추가하기 위해 대기한 시간의 비율',
    datasource=prometheus,
    fill=1,
  )
  .addTargets([
    prometheus.target(
      expr='kafka_producer_bufferpool_wait_ratio',
      intervalFactor=1,
      legendFormat='{{instance}}'
    ),
  ]) + { gridPos: { h: 8, w: 8, x: 0, y: 10 } },
  graphPanel.new(
    title='IO Wait Time(ns)',
    description='CPU가 I/O 작업 완료까지 기다리(idle) 평균 시간',
    fill=1,
    datasource=prometheus,
  )
  .addTargets([
    prometheus.target(
      expr='kafka_producer_io_wait_time_ns_avg',
      intervalFactor=1,
      legendFormat='{{instance}}'
    ),
  ]) + { gridPos: { h: 8, w: 8, x: 8, y: 10 } },
  graphPanel.new(
    title='Record Queue Waiting Average Time(ms)',
    description='프로듀서가 레코드큐에 대기하는 평균 시간(ms)',
    fill=1,
    datasource=prometheus,
  )
  .addTargets([
    prometheus.target(
      expr='kafka_producer_record_queue_time_avg',
      intervalFactor=1,
      legendFormat='{{instance}}'
    ),
  ]) + { gridPos: { h: 8, w: 8, x: 16, y: 10 } },
  //################ Row ##################
  textPanel.new(
    mode='html',
    content='<h2><center>Sender 구간</center></h2>',
  ) + { gridPos: { h: 2, w: 24, x: 0, y: 18 } },
  //################ Row ##################
  graphPanel.new(
    title='Connection Count',
    description='브로커와 커넥션 수',
    fill=1,
    datasource=prometheus,
  )
  .addTargets([
    prometheus.target(
      expr='kafka_producer_connection_count',
      intervalFactor=1,
      legendFormat='{{instance}}'
    ),
  ]) + { gridPos: { h: 8, w: 8, x: 0, y: 20 } },
  graphPanel.new(
    title='Select Rate',
    description='브로커가 전송할 데이터가 있는지 확인한 횟수',
    fill=1,
    datasource=prometheus,
  )
  .addTargets([
    prometheus.target(
      expr='kafka_producer_select_rate',
      intervalFactor=1,
      legendFormat='{{instance}}'
    ),
  ]) + { gridPos: { h: 8, w: 8, x: 8, y: 20 } },
  graphPanel.new(
    title='Record Error Rate',
    description='레코드 전송 실패 비율',
    fill=1,
    datasource=prometheus,
  )
  .addTargets([
    prometheus.target(
      expr='kafka_producer_record_error_rate',
      intervalFactor=1,
      legendFormat='{{instance}}'
    ),
  ]) + { gridPos: { h: 8, w: 8, x: 16, y: 20 } },
  //################ Row ##################
  textPanel.new(
    mode='html',
    content='<h2><center>Broker 전송 구간</center></h2>',
  ) + { gridPos: { h: 2, w: 24, x: 0, y: 28 } },
  //################ Row ##################
  graphPanel.new(
    title='Record Send Rate',
    description='초당 전송되는 레코드 수',
    fill=1,
    datasource=prometheus,
  )
  .addTargets([
    prometheus.target(
      expr='kafka_producer_record_send_rate',
      intervalFactor=0,
      legendFormat='{{instance}}'
    ),
    prometheus.target(
      expr='sum(kafka_producer_record_send_rate)',
      intervalFactor=1,
      legendFormat='total'
    ),
  ]) + { gridPos: { h: 8, w: 8, x: 0, y: 30 } },
  graphPanel.new(
    title='Outgoing Record bytes',
    description='초당 전송되는 레코드 사이즈',
    fill=1,
    datasource=prometheus,
  )
  .addTargets([
    prometheus.target(
      expr='sum(kafka_producer_node_outgoing_byte_rate)',
      intervalFactor=1,
      legendFormat='{{instance}}'
    ),
  ]) + { gridPos: { h: 8, w: 8, x: 8, y: 30 } },
  graphPanel.new(
    title='Request Latency',
    description='요청 후 응답받는 평균 시간',
    fill=1,
    datasource=prometheus,
  )
  .addTargets([
    prometheus.target(
      expr='kafka_producer_node_request_latency_avg',
      intervalFactor=1,
      legendFormat='{{node_id}}'
    ),
  ]) + { gridPos: { h: 8, w: 8, x: 16, y: 30 } },
])
