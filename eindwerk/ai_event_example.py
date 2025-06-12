import asyncio
import time
import random

# Check if we're on MicroPython
import sys
is_micropython = sys.implementation.name == 'micropython'

# Use the appropriate event loop policy
if is_micropython:
    # MicroPython has a different asyncio implementation
    pass
else:
    # For CPython, use the default event loop policy
    asyncio.set_event_loop_policy(asyncio.DefaultEventLoopPolicy())

async def producer(event, delay_range=(1, 3)):
    """
    Producer task that periodically sets the event
    
    Parameters:
    -----------
    event : asyncio.Event
        The event to set
    delay_range : tuple
        Min and max delay between events in seconds
    """
    while True:
        # Random delay to simulate work
        delay = random.uniform(delay_range[0], delay_range[1])
        print(f"Producer: Working for {delay:.1f} seconds...")
        await asyncio.sleep(delay)
        
        # Set the event to signal consumers
        print("Producer: Setting event")
        event.set()
        
        # Wait for consumers to process
        await asyncio.sleep(0.5)
        
        # Clear the event for the next cycle
        print("Producer: Clearing event")
        event.clear()

async def consumer(name, event, process_time=1):
    """
    Consumer task that waits for the event
    
    Parameters:
    -----------
    name : str
        Consumer name for identification
    event : asyncio.Event
        The event to wait for
    process_time : float
        Time to process after event is set
    """
    while True:
        print(f"Consumer {name}: Waiting for event...")
        await event.wait()  # Wait until the event is set
        
        print(f"Consumer {name}: Event received, processing...")
        await asyncio.sleep(process_time)  # Simulate processing time
        
        print(f"Consumer {name}: Processing complete")

async def timeout_waiter(event, timeout=5):
    """
    Demonstrates waiting for an event with a timeout
    
    Parameters:
    -----------
    event : asyncio.Event
        The event to wait for
    timeout : float
        Maximum time to wait in seconds
    """
    print(f"Timeout waiter: Starting with {timeout}s timeout")
    
    try:
        # Create a task for waiting for the event
        wait_task = asyncio.create_task(event.wait())
        
        # Wait for either the event or the timeout
        done, pending = await asyncio.wait([wait_task], timeout=timeout)
        
        if wait_task in done:
            print("Timeout waiter: Event was set!")
            return True
        else:
            print("Timeout waiter: Timeout occurred")
            return False
            
    except AttributeError:
        # For older MicroPython versions without asyncio.wait
        start_time = time.time()
        while not event.is_set():
            await asyncio.sleep(0.1)
            if time.time() - start_time > timeout:
                print("Timeout waiter: Timeout occurred")
                return False
        
        print("Timeout waiter: Event was set!")
        return True

async def conditional_waiter(event, condition_func):
    """
    Waits for an event and checks a condition
    
    Parameters:
    -----------
    event : asyncio.Event
        The event to wait for
    condition_func : callable
        Function that returns True/False to check after event is set
    """
    while True:
        # Wait for the event
        await event.wait()
        
        # Check the condition
        if condition_func():
            print("Conditional waiter: Condition met!")
            # Do something when condition is met
            await asyncio.sleep(0.2)
        else:
            print("Conditional waiter: Condition not met, waiting again")
        
        # Wait a bit before checking again
        await asyncio.sleep(0.5)

async def event_monitor(event, check_interval=1):
    """
    Monitors the state of an event
    
    Parameters:
    -----------
    event : asyncio.Event
        The event to monitor
    check_interval : float
        How often to check the event state
    """
    while True:
        state = "SET" if event.is_set() else "CLEAR"
        print(f"Monitor: Event is {state}")
        await asyncio.sleep(check_interval)

async def event_toggler(event, toggle_interval=4):
    """
    Toggles an event at regular intervals
    
    Parameters:
    -----------
    event : asyncio.Event
        The event to toggle
    toggle_interval : float
        How often to toggle the event
    """
    while True:
        await asyncio.sleep(toggle_interval)
        
        if event.is_set():
            print("Toggler: Clearing event")
            event.clear()
        else:
            print("Toggler: Setting event")
            event.set()

async def main():
    """Main function that sets up and runs all tasks"""
    # Create an event
    event = asyncio.Event()
    
    # Create a condition function for the conditional waiter
    counter = 0
    def condition_check():
        nonlocal counter
        counter += 1
        return counter % 3 == 0  # True every third time
    
    # Set up tasks
    tasks = [
        asyncio.create_task(producer(event)),
        asyncio.create_task(consumer("A", event, 0.5)),
        asyncio.create_task(consumer("B", event, 1.0)),
        asyncio.create_task(event_monitor(event, 2)),
        asyncio.create_task(conditional_waiter(event, condition_check))
    ]
    
    # Run a timeout waiter once
    print("\n--- Running timeout waiter ---")
    timeout_result = await timeout_waiter(asyncio.Event(), 3)  # New event that won't be set
    print(f"Timeout waiter result: {timeout_result}")
    
    # Run another timeout waiter with an event that will be set
    print("\n--- Running another timeout waiter ---")
    quick_event = asyncio.Event()
    
    # Create a task to set the event after 1 second
    async def delayed_set(evt, delay):
        await asyncio.sleep(delay)
        print(f"Setting event after {delay}s delay")
        evt.set()
    
    asyncio.create_task(delayed_set(quick_event, 1))
    timeout_result = await timeout_waiter(quick_event, 3)
    print(f"Timeout waiter result: {timeout_result}")
    
    # Run the main event demo
    print("\n--- Running main event demo ---")
    try:
        # Wait for all tasks to complete (they won't, we'll need to cancel)
        await asyncio.gather(*tasks)
    except asyncio.CancelledError:
        pass

# Run on MicroPython
if __name__ == "__main__":
    try:
        print("Starting asyncio event example...")
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Program interrupted")

