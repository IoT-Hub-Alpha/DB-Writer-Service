from IoTKafka import IoTKafkaConsumer


def run_writer():
    consumer = IoTKafkaConsumer(group_id="db_writer")
    consumer.subscribe(["telemetry.clean"])
    
    write_buffer = WriteBuffer(consumer, 1.0, 2000)
    
    while True:
        write_buffer.handle()



if __name__ == "__main__":
    run_writer()