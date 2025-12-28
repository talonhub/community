#!/usr/bin/env python3
"""Performance test script to measure screenshot capture time."""

import time
from statistics import mean, stdev

from PIL import Image, ImageGrab

# Import MSS at module level like the actual code
try:
    import mss
except ImportError:
    mss = None

# Import DXcam at module level
try:
    import dxcam
except ImportError:
    dxcam = None


def test_pil_imagegrab_performance(num_iterations=10, warmup_iterations=3):
    """Test PIL ImageGrab performance."""
    # Warmup iterations
    for _ in range(warmup_iterations):
        screenshot = ImageGrab.grab()
        screenshot.load()

    times = []

    for i in range(num_iterations):
        start_time = time.perf_counter()
        screenshot = ImageGrab.grab()
        # Force image loading for consistent measurement
        screenshot.load()
        end_time = time.perf_counter()

        capture_time = (end_time - start_time) * 1000  # Convert to milliseconds
        times.append(capture_time)
        print(f"Iteration {i + 1}: {capture_time:.2f}ms")

    avg_time = mean(times)
    std_time = stdev(times) if len(times) > 1 else 0

    print(f"\nPIL ImageGrab Results ({num_iterations} iterations):")
    print(f"Average time: {avg_time:.2f}ms")
    print(f"Standard deviation: {std_time:.2f}ms")
    print(f"Min time: {min(times):.2f}ms")
    print(f"Max time: {max(times):.2f}ms")

    return avg_time, std_time


def test_mss_performance(num_iterations=10, warmup_iterations=3):
    """Test MSS performance matching actual code behavior."""
    if not mss:
        print("MSS not available - skipping MSS performance test")
        return None, None

    # Warmup iterations
    for _ in range(warmup_iterations):
        with mss.mss() as sct:
            monitor = sct.monitors[1]
            screenshot = sct.grab(monitor)
            img = Image.frombytes(
                "RGB", screenshot.size, screenshot.bgra, "raw", "BGRX"
            )
            img.load()

    times = []

    for i in range(num_iterations):
        start_time = time.perf_counter()
        # Match actual code: create context manager for each screenshot
        with mss.mss() as sct:
            monitor = sct.monitors[1]  # Primary monitor
            screenshot = sct.grab(monitor)
            # Convert to PIL Image for consistency with current code
            img = Image.frombytes(
                "RGB", screenshot.size, screenshot.bgra, "raw", "BGRX"
            )
            img.load()
        end_time = time.perf_counter()

        capture_time = (end_time - start_time) * 1000  # Convert to milliseconds
        times.append(capture_time)
        print(f"Iteration {i + 1}: {capture_time:.2f}ms")

    avg_time = mean(times)
    std_time = stdev(times) if len(times) > 1 else 0

    print(f"\nMSS Results ({num_iterations} iterations):")
    print(f"Average time: {avg_time:.2f}ms")
    print(f"Standard deviation: {std_time:.2f}ms")
    print(f"Min time: {min(times):.2f}ms")
    print(f"Max time: {max(times):.2f}ms")

    return avg_time, std_time


def test_dxcam_performance(num_iterations=10, warmup_iterations=3):
    """Test DXcam performance."""
    if not dxcam:
        print("DXcam not available - skipping DXcam performance test")
        return None, None

    # Create camera once (similar to how it would be used in practice)
    camera = dxcam.create()
    if camera is None:
        print("DXcam camera creation failed - skipping DXcam performance test")
        return None, None

    try:
        # Warmup iterations
        for _ in range(warmup_iterations):
            frame = camera.grab()
            if frame is not None:
                # Convert to PIL Image for consistency
                img = Image.fromarray(frame)
                img.load()

        times = []

        for i in range(num_iterations):
            start_time = time.perf_counter()
            frame = camera.grab()
            if frame is not None:
                # Convert to PIL Image for consistency with other tests
                img = Image.fromarray(frame)
                img.load()
            end_time = time.perf_counter()

            capture_time = (end_time - start_time) * 1000  # Convert to milliseconds
            times.append(capture_time)
            print(f"Iteration {i + 1}: {capture_time:.2f}ms")

        avg_time = mean(times)
        std_time = stdev(times) if len(times) > 1 else 0

        print(f"\nDXcam Results ({num_iterations} iterations):")
        print(f"Average time: {avg_time:.2f}ms")
        print(f"Standard deviation: {std_time:.2f}ms")
        print(f"Min time: {min(times):.2f}ms")
        print(f"Max time: {max(times):.2f}ms")

        return avg_time, std_time

    finally:
        # Clean up camera
        camera.release()


if __name__ == "__main__":
    print("Screenshot Performance Test")
    print("=" * 40)

    # Test PIL ImageGrab
    pil_avg, pil_std = test_pil_imagegrab_performance()

    print("\n" + "=" * 40)

    # Test MSS
    mss_avg, mss_std = test_mss_performance()

    print("\n" + "=" * 40)

    # Test DXcam
    dxcam_avg, dxcam_std = test_dxcam_performance()

    # Compare results
    print("\n" + "=" * 40)
    print("COMPARISON:")
    print(f"PIL ImageGrab: {pil_avg:.2f}ms ± {pil_std:.2f}ms")

    results = [("PIL ImageGrab", pil_avg)]

    if mss_avg is not None:
        print(f"MSS:           {mss_avg:.2f}ms ± {mss_std:.2f}ms")
        results.append(("MSS", mss_avg))

    if dxcam_avg is not None:
        print(f"DXcam:         {dxcam_avg:.2f}ms ± {dxcam_std:.2f}ms")
        results.append(("DXcam", dxcam_avg))

    # Find the fastest method
    if len(results) > 1:
        fastest = min(results, key=lambda x: x[1])
        print(f"\nFastest method: {fastest[0]} ({fastest[1]:.2f}ms)")

        # Show improvements relative to PIL ImageGrab
        print("\nRelative to PIL ImageGrab:")
        for name, avg_time in results:
            if name != "PIL ImageGrab":
                improvement = pil_avg - avg_time
                improvement_percent = (improvement / pil_avg) * 100
                if improvement > 0:
                    print(
                        f"{name}: {improvement:.2f}ms faster ({improvement_percent:.1f}% improvement)"
                    )
                else:
                    print(
                        f"{name}: {-improvement:.2f}ms slower ({-improvement_percent:.1f}% worse)"
                    )
