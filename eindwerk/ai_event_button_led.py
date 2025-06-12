import asyncio
import machine
import time

class AsyncButton:
    def __init__(self, pin, debounce_ms=50):
        """
        Asynchronous button handler with debouncing
        
        Parameters:
        -----------
        pin : int
            GPIO pin number for the button
        debounce_ms : int
            Debounce time in milliseconds
        """
        self.pin = machine.Pin(pin, machine.Pin.IN, machine.Pin.PULL_UP)
        self.debounce_ms = debounce_ms
        self.pressed_event = asyncio.Event()
        self.last_press_time = 0
        self._task = None
    
    async def _monitor(self):
        """Monitor the button state and set event when pressed"""
        while True:
            # Button pressed (pin goes LOW with pull-up)
            if self.pin.value() == 0:
                current_time = time.ticks_ms()
                if time.ticks_diff(current_time, self.last_press_time) > self.debounce_ms:
                    self.last_press_time = current_time
                    print("Button pressed")
                    self.pressed_event.set()
                
                # Wait for button release
                while self.pin.value() == 0:
                    await asyncio.sleep_ms(10)
            
            await asyncio.sleep_ms(20)
    
    def start_monitoring(self):
        """Start monitoring the button in the background"""
        if self._task is None:
            self._task = asyncio.create_task(self._monitor())
    
    def stop_monitoring(self):
        """Stop monitoring the button"""
        if self._task is not None:
            self._task.cancel()
            self._task = None

class AsyncLED:
    def __init__(self, pin):
        """
        Asynchronous LED controller
        
        Parameters:
        -----------
        pin : int
            GPIO pin number for the LED
        """
        self.pin = machine.Pin(pin, machine.Pin.OUT)
        self.pin.off()  # Start with LED off
    
    def on(self):
        """Turn the LED on"""
        self.pin.on()
    
    def off(self):
        """Turn the LED off"""
        self.pin.off()
    
    async def blink(self, count=3, on_time_ms=200, off_time_ms=200):
        """
        Blink the LED a specified number of times
        
        Parameters:
        -----------
        count : int
            Number of blinks
        on_time_ms : int
            Time LED stays on in milliseconds
        off_time_ms : int
            Time LED stays off in milliseconds
        """
        for _ in range(count):
            self.on()
            await asyncio.sleep_ms(on_time_ms)
            self.off()
            await asyncio.sleep_ms(off_time_ms)
    
    async def pulse(self, duration_ms=1000, steps=50):
        """
        Pulse the LED using PWM
        
        Parameters:
        -----------
        duration_ms : int
            Total duration of the pulse
        steps : int
            Number of brightness steps
        """
        # Create PWM object
        pwm = machine.PWM(self.pin)
        pwm.freq(1000)  # 1 kHz frequency
        
        step_time = duration_ms // (steps * 2)
        
        # Ramp up
        for i in range(steps):
            duty = int((i / steps) * 1023)  # 0 to 1023 for ESP8266
            pwm.duty(duty)
            await asyncio.sleep_ms(step_time)
        
        # Ramp down
        for i in range(steps, 0, -1):
            duty = int((i / steps) * 1023)
            pwm.duty(duty)
            await asyncio.sleep_ms(step_time)
        
        # Clean up
        pwm.deinit()
        self.off()

async def button_led_demo():
    """Demo using button event to control LEDs"""
    # Initialize button and LEDs
    button = AsyncButton(pin=0)  # GPIO0 for button
    led1 = AsyncLED(pin=5)       # GPIO5 for LED 1
    led2 = AsyncLED(pin=4)       # GPIO4 for LED 2
    
    # Start button monitoring
    button.start_monitoring()
    
    print("Press the button to trigger LED actions")
    
    try:
        while True:
            # Wait for button press event
            await button.pressed_event.wait()
            print("Button event received")
            
            # Clear the event for the next press
            button.pressed_event.clear()
            
            # Perform LED actions
            led_tasks = [
                asyncio.create_task(led1.blink(3, 200, 200)),
                asyncio.create_task(led2.pulse(1500))
            ]
            
            # Wait for all LED actions to complete
            await asyncio.gather(*led_tasks)
            
    except asyncio.CancelledError:
        button.stop_monitoring()
        led1.off()
        led2.off()
        raise

async def multiple_events_demo():
    """Demo using multiple events for synchronization"""
    # Create events
    data_ready = asyncio.Event()
    processing_done = asyncio.Event()
    shutdown_requested = asyncio.Event()
    
    async def data_producer():
        """Simulates a data source"""
        counter = 0
        while not shutdown_requested.is_set():
            # Generate some data
            await asyncio.sleep(1)
            counter += 1
            print(f"Producer: Data #{counter} ready")
            
            # Signal that data is ready
            data_ready.set()
            
            # Wait for processing to complete
            await processing_done.wait()
            processing_done.clear()
            
            # Check if we should shut down
            if counter >= 5:
                print("Producer: Requesting shutdown")
                shutdown_requested.set()
    
    async def data_processor():
        """Processes data when it's ready"""
        while not shutdown_requested.is_set():
            # Wait for data to be ready
            await data_ready.wait()
            data_ready.clear()
            
            # Process the data
            print("Processor: Processing data...")
            await asyncio.sleep(0.5)
            print("Processor: Processing complete")
            
            # Signal that processing is done
            processing_done.set()
    
    async def system_monitor():
        """Monitors system status"""
        while not shutdown_requested.is_set():
            print("Monitor: System running normally")
            await asyncio.sleep(2)
        
        print("Monitor: Shutdown requested, cleaning up...")
    
    # Create and run tasks
    tasks = [
        asyncio.create_task(data_producer()),
        asyncio.create_task(data_processor()),
        asyncio.create_task(system_monitor())
    ]
    
    # Wait for shutdown request
    await shutdown_requested.wait()
    print("Main: Shutdown requested, waiting for tasks to complete")
    
    # Give tasks time to finish
    await asyncio.sleep(1)
    
    # Cancel all tasks
    for task in tasks:
        task.cancel()
    
    # Wait for tasks to be cancelled
    try:
        await asyncio.gather(*tasks)
    except asyncio.CancelledError:
        pass
    
    print("Main: All tasks cancelled, shutdown complete")

# Run the demo
if __name__ == "__main__":
    try:
        print("Starting asyncio Event demo...")
        
        # Choose which demo to run
        # asyncio.run(button_led_demo())
        asyncio.run(multiple_events_demo())
        
    except KeyboardInterrupt:
        print("Program interrupted")

