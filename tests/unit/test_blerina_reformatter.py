import unittest
import numpy as np
from blerina_reformatter import classify_quality, remove_artifacts, calculate_statistics, generate_hash

class TestBlerinaReformatter(unittest.TestCase):

    def setUp(self):
        self.signal = [1, 2, 3, 4, 100, 5, 6, 7, 8, 9]
        self.snr_thresholds = {
            "EXCELLENT": 20,
            "GOOD": 15,
            "ACCEPTABLE": 10,
            "DEGRADED": 5,
            "CRITICAL": 1,
            "UNUSABLE": 0,  # Include UNUSABLE for testing
        }

    def test_classify_quality(self):
        quality = classify_quality(self.signal, self.snr_thresholds)
        self.assertIn(quality, self.snr_thresholds.keys())

    def test_remove_artifacts(self):
        cleaned_signal = remove_artifacts(self.signal)

        # Log debug information for troubleshooting
        print(f"Original Signal: {self.signal}")
        print(f"Cleaned Signal: {cleaned_signal}")

        # Calculate bounds dynamically for validation
        q1, q3 = np.percentile(self.signal, [25, 75])
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr

        # Ensure cleaned signal is not empty
        self.assertTrue(len(cleaned_signal) > 0, "Cleaned signal should not be empty")

        # Validate that all values are within dynamically calculated bounds
        self.assertTrue(
            all(lower_bound <= x <= upper_bound for x in cleaned_signal),
            f"Values in cleaned signal should be between {lower_bound} and {upper_bound}"
        )

    def test_calculate_statistics(self):
        stats = calculate_statistics(self.signal)
        self.assertAlmostEqual(stats["mean"], np.mean(self.signal))
        self.assertAlmostEqual(stats["median"], np.median(self.signal))
        self.assertAlmostEqual(stats["variance"], np.var(self.signal))
        self.assertAlmostEqual(stats["std_dev"], np.std(self.signal))

    def test_generate_hash(self):
        hash_value = generate_hash(self.signal)
        self.assertEqual(len(hash_value), 64)  # SHA-256 hash length

if __name__ == "__main__":
    unittest.main()

