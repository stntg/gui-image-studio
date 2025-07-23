Batch Operations
================

This guide covers batch processing capabilities in GUI Image Studio, including processing multiple images, automating workflows, and creating efficient batch processing systems.

Overview of Batch Processing
-----------------------------

GUI Image Studio provides several approaches to batch processing:

- **Built-in batch functions** for common operations
- **Command-line tools** for automation
- **Python API** for custom batch processing
- **Folder-based processing** with recursive support
- **Progress tracking** and error handling
- **Parallel processing** for improved performance

Built-in Batch Functions
------------------------

embed_images_from_folder()
~~~~~~~~~~~~~~~~~~~~~~~~~~

The primary batch function for creating embedded image resources:

.. code-block:: python

    from gui_image_studio import embed_images_from_folder

    # Basic batch embedding
    embed_images_from_folder(
        folder_path="images/",
        output_file="embedded_images.py",
        compression_quality=85
    )

**Advanced Usage:**

.. code-block:: python

    # Process with specific settings
    embed_images_from_folder(
        folder_path="assets/icons/",
        output_file="src/resources/icons.py",
        compression_quality=95  # High quality for icons
    )

    # Process photos with compression
    embed_images_from_folder(
        folder_path="photos/",
        output_file="src/resources/photos.py",
        compression_quality=75  # Lower quality for photos
    )

create_sample_images()
~~~~~~~~~~~~~~~~~~~~~~

Batch creation of sample images for testing:

.. code-block:: python

    from gui_image_studio import create_sample_images

    # Create default samples
    create_sample_images()

    # Create in specific directory
    create_sample_images(output_dir="test_images")

Command-Line Batch Processing
-----------------------------

GUI Image Studio Generator
~~~~~~~~~~~~~~~~~~~~~~~~~~

The command-line generator provides powerful batch processing:

.. code-block:: bash

    # Basic folder processing
    gui-image-studio-generate --folder images/ --output embedded.py

    # High-quality processing
    gui-image-studio-generate \
      --folder assets/ \
      --output resources.py \
      --quality 95

    # Recursive processing
    gui-image-studio-generate \
      --folder project/ \
      --output all_images.py \
      --quality 80 \
      --recursive

**Advanced Command-Line Options:**

.. code-block:: bash

    # Process specific formats only
    gui-image-studio-generate \
      --folder icons/ \
      --output icons.py \
      --formats png,svg \
      --quality 100

    # Exclude certain patterns
    gui-image-studio-generate \
      --folder images/ \
      --output processed.py \
      --exclude "*.tmp,*_backup.*" \
      --quality 85

Batch Sample Creation
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    # Create samples in specific directory
    gui-image-studio-create-samples --output test_data/

    # Create specific number of samples
    gui-image-studio-create-samples --count 20 --output samples/

    # Create samples with specific dimensions
    gui-image-studio-create-samples --size 256x256 --output large_samples/

Custom Batch Processing
-----------------------

Basic Batch Processing Class
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import os
    from pathlib import Path
    from gui_image_studio import get_image

    class ImageBatchProcessor:
        def __init__(self, framework="tkinter"):
            self.framework = framework
            self.supported_formats = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.webp'}
            self.processed_count = 0
            self.error_count = 0
            self.errors = []

        def process_folder(self, input_folder, output_folder, transformations,
                          recursive=False, progress_callback=None):
            """
            Process all images in a folder with given transformations.

            Args:
                input_folder: Source folder path
                output_folder: Destination folder path
                transformations: Dict of transformation parameters
                recursive: Process subfolders
                progress_callback: Function to call with progress updates
            """

            # Create output folder
            os.makedirs(output_folder, exist_ok=True)

            # Get all image files
            image_files = self._find_image_files(input_folder, recursive)
            total_files = len(image_files)

            print(f"Found {total_files} image files to process")

            # Process each file
            for i, file_path in enumerate(image_files):
                try:
                    self._process_single_file(
                        file_path,
                        input_folder,
                        output_folder,
                        transformations
                    )
                    self.processed_count += 1

                except Exception as e:
                    self.error_count += 1
                    self.errors.append(f"{file_path}: {str(e)}")
                    print(f"Error processing {file_path}: {e}")

                # Progress callback
                if progress_callback:
                    progress_callback(i + 1, total_files)

            return self._get_summary()

        def _find_image_files(self, folder, recursive):
            """Find all image files in folder."""
            image_files = []

            if recursive:
                for root, dirs, files in os.walk(folder):
                    for file in files:
                        if Path(file).suffix.lower() in self.supported_formats:
                            image_files.append(os.path.join(root, file))
            else:
                for file in os.listdir(folder):
                    if Path(file).suffix.lower() in self.supported_formats:
                        image_files.append(os.path.join(folder, file))

            return image_files

        def _process_single_file(self, file_path, input_folder, output_folder, transformations):
            """Process a single image file."""

            # Calculate relative path for output
            rel_path = os.path.relpath(file_path, input_folder)
            output_path = os.path.join(output_folder, rel_path)

            # Create output subdirectory if needed
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            # Process image
            processed_image = get_image(
                file_path,
                framework=self.framework,
                **transformations
            )

            print(f"Processed: {rel_path}")

        def _get_summary(self):
            """Get processing summary."""
            return {
                'processed': self.processed_count,
                'errors': self.error_count,
                'error_list': self.errors,
                'success_rate': (self.processed_count / (self.processed_count + self.error_count)) * 100
                if (self.processed_count + self.error_count) > 0 else 0
            }

    # Usage example
    def process_photo_collection():
        processor = ImageBatchProcessor("tkinter")

        transformations = {
            'size': (800, 600),
            'contrast': 1.1,
            'saturation': 1.05,
            'tint_color': (255, 245, 235),
            'tint_intensity': 0.05
        }

        def progress_callback(current, total):
            percent = (current / total) * 100
            print(f"Progress: {current}/{total} ({percent:.1f}%)")

        summary = processor.process_folder(
            input_folder="raw_photos/",
            output_folder="processed_photos/",
            transformations=transformations,
            recursive=True,
            progress_callback=progress_callback
        )

        print(f"\nProcessing complete:")
        print(f"  Processed: {summary['processed']} files")
        print(f"  Errors: {summary['errors']} files")
        print(f"  Success rate: {summary['success_rate']:.1f}%")

Advanced Batch Processing
-------------------------

Multi-Format Batch Processor
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    class AdvancedBatchProcessor:
        def __init__(self, framework="tkinter"):
            self.framework = framework
            self.format_configs = {
                'icons': {
                    'size': (64, 64),
                    'quality': 95,
                    'formats': ['.png', '.ico']
                },
                'photos': {
                    'size': (1200, 800),
                    'quality': 80,
                    'formats': ['.jpg', '.jpeg']
                },
                'thumbnails': {
                    'size': (150, 150),
                    'quality': 70,
                    'formats': ['.jpg', '.png']
                }
            }

        def process_by_type(self, input_folder, output_base, type_configs=None):
            """Process images by type with different settings."""

            if type_configs is None:
                type_configs = self.format_configs

            results = {}

            for image_type, config in type_configs.items():
                print(f"\nProcessing {image_type}...")

                output_folder = os.path.join(output_base, image_type)

                # Filter files by format
                image_files = self._find_files_by_format(
                    input_folder,
                    config['formats']
                )

                if not image_files:
                    print(f"No {image_type} files found")
                    continue

                # Process files
                type_results = self._process_file_list(
                    image_files,
                    output_folder,
                    {
                        'size': config['size'],
                        'contrast': config.get('contrast', 1.0),
                        'saturation': config.get('saturation', 1.0)
                    }
                )

                results[image_type] = type_results

            return results

        def _find_files_by_format(self, folder, formats):
            """Find files matching specific formats."""
            files = []
            for file in os.listdir(folder):
                if Path(file).suffix.lower() in formats:
                    files.append(os.path.join(folder, file))
            return files

        def _process_file_list(self, file_list, output_folder, transformations):
            """Process a list of files."""
            os.makedirs(output_folder, exist_ok=True)

            processed = 0
            errors = 0

            for file_path in file_list:
                try:
                    filename = os.path.basename(file_path)
                    output_path = os.path.join(output_folder, filename)

                    # Process image
                    processed_image = get_image(
                        file_path,
                        framework=self.framework,
                        **transformations
                    )

                    processed += 1
                    print(f"  Processed: {filename}")

                except Exception as e:
                    errors += 1
                    print(f"  Error processing {filename}: {e}")

            return {'processed': processed, 'errors': errors}

    # Usage
    def organize_and_process_images():
        processor = AdvancedBatchProcessor("customtkinter")

        # Custom configurations for different image types
        configs = {
            'app_icons': {
                'size': (128, 128),
                'quality': 100,
                'formats': ['.png'],
                'contrast': 1.0,
                'saturation': 1.0
            },
            'web_images': {
                'size': (800, 600),
                'quality': 75,
                'formats': ['.jpg', '.jpeg'],
                'contrast': 1.1,
                'saturation': 1.05
            },
            'thumbnails': {
                'size': (200, 200),
                'quality': 60,
                'formats': ['.jpg', '.png'],
                'contrast': 1.0,
                'saturation': 1.0
            }
        }

        results = processor.process_by_type(
            input_folder="mixed_images/",
            output_base="organized_output/",
            type_configs=configs
        )

        # Print summary
        for image_type, result in results.items():
            print(f"{image_type}: {result['processed']} processed, {result['errors']} errors")

Parallel Batch Processing
-------------------------

Threading-Based Processing
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import threading
    from concurrent.futures import ThreadPoolExecutor, as_completed
    from queue import Queue

    class ParallelBatchProcessor:
        def __init__(self, framework="tkinter", max_workers=4):
            self.framework = framework
            self.max_workers = max_workers
            self.progress_queue = Queue()
            self.results_lock = threading.Lock()
            self.processed_count = 0
            self.error_count = 0
            self.errors = []

        def process_folder_parallel(self, input_folder, output_folder,
                                  transformations, progress_callback=None):
            """Process folder using multiple threads."""

            # Find all image files
            image_files = self._find_image_files(input_folder)
            total_files = len(image_files)

            print(f"Processing {total_files} files with {self.max_workers} workers")

            # Create output folder
            os.makedirs(output_folder, exist_ok=True)

            # Process files in parallel
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                # Submit all tasks
                future_to_file = {
                    executor.submit(
                        self._process_single_file_safe,
                        file_path,
                        input_folder,
                        output_folder,
                        transformations
                    ): file_path
                    for file_path in image_files
                }

                # Process completed tasks
                completed = 0
                for future in as_completed(future_to_file):
                    file_path = future_to_file[future]
                    completed += 1

                    try:
                        result = future.result()
                        if result['success']:
                            with self.results_lock:
                                self.processed_count += 1
                        else:
                            with self.results_lock:
                                self.error_count += 1
                                self.errors.append(f"{file_path}: {result['error']}")

                    except Exception as e:
                        with self.results_lock:
                            self.error_count += 1
                            self.errors.append(f"{file_path}: {str(e)}")

                    # Progress callback
                    if progress_callback:
                        progress_callback(completed, total_files)

            return self._get_summary()

        def _process_single_file_safe(self, file_path, input_folder,
                                    output_folder, transformations):
            """Thread-safe single file processing."""
            try:
                # Calculate output path
                rel_path = os.path.relpath(file_path, input_folder)
                output_path = os.path.join(output_folder, rel_path)

                # Create output directory
                os.makedirs(os.path.dirname(output_path), exist_ok=True)

                # Process image
                processed_image = get_image(
                    file_path,
                    framework=self.framework,
                    **transformations
                )

                return {'success': True, 'file': file_path}

            except Exception as e:
                return {'success': False, 'file': file_path, 'error': str(e)}

        def _find_image_files(self, folder):
            """Find all image files in folder."""
            supported_formats = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff'}
            image_files = []

            for file in os.listdir(folder):
                if Path(file).suffix.lower() in supported_formats:
                    image_files.append(os.path.join(folder, file))

            return image_files

        def _get_summary(self):
            """Get processing summary."""
            total = self.processed_count + self.error_count
            return {
                'processed': self.processed_count,
                'errors': self.error_count,
                'error_list': self.errors,
                'success_rate': (self.processed_count / total) * 100 if total > 0 else 0
            }

    # Usage example
    def fast_batch_processing():
        processor = ParallelBatchProcessor("tkinter", max_workers=8)

        transformations = {
            'size': (400, 300),
            'contrast': 1.2,
            'saturation': 1.1
        }

        def progress_callback(current, total):
            percent = (current / total) * 100
            print(f"\rProgress: {current}/{total} ({percent:.1f}%)", end='', flush=True)

        summary = processor.process_folder_parallel(
            input_folder="large_image_collection/",
            output_folder="processed_collection/",
            transformations=transformations,
            progress_callback=progress_callback
        )

        print(f"\n\nParallel processing complete:")
        print(f"  Processed: {summary['processed']} files")
        print(f"  Errors: {summary['errors']} files")
        print(f"  Success rate: {summary['success_rate']:.1f}%")

Batch Processing Workflows
---------------------------

Image Optimization Workflow
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    class ImageOptimizationWorkflow:
        def __init__(self, framework="tkinter"):
            self.framework = framework
            self.optimization_profiles = {
                'web_optimized': {
                    'max_size': (1200, 800),
                    'quality': 75,
                    'contrast': 1.05,
                    'saturation': 1.02
                },
                'thumbnail': {
                    'max_size': (300, 300),
                    'quality': 70,
                    'contrast': 1.0,
                    'saturation': 1.0
                },
                'icon': {
                    'max_size': (128, 128),
                    'quality': 95,
                    'contrast': 1.0,
                    'saturation': 1.0
                },
                'print_ready': {
                    'max_size': (3000, 2000),
                    'quality': 95,
                    'contrast': 1.1,
                    'saturation': 1.05
                }
            }

        def optimize_folder(self, input_folder, output_base, profiles=None):
            """Optimize images for different use cases."""

            if profiles is None:
                profiles = list(self.optimization_profiles.keys())

            results = {}

            for profile_name in profiles:
                if profile_name not in self.optimization_profiles:
                    print(f"Unknown profile: {profile_name}")
                    continue

                profile = self.optimization_profiles[profile_name]
                output_folder = os.path.join(output_base, profile_name)

                print(f"\nOptimizing for {profile_name}...")

                result = self._optimize_with_profile(
                    input_folder,
                    output_folder,
                    profile
                )

                results[profile_name] = result

            return results

        def _optimize_with_profile(self, input_folder, output_folder, profile):
            """Optimize images with a specific profile."""

            os.makedirs(output_folder, exist_ok=True)

            # Find image files
            image_files = []
            for file in os.listdir(input_folder):
                if Path(file).suffix.lower() in {'.png', '.jpg', '.jpeg', '.gif', '.bmp'}:
                    image_files.append(os.path.join(input_folder, file))

            processed = 0
            errors = 0

            for file_path in image_files:
                try:
                    filename = os.path.basename(file_path)
                    output_path = os.path.join(output_folder, filename)

                    # Apply optimization
                    optimized_image = get_image(
                        file_path,
                        framework=self.framework,
                        size=profile['max_size'],
                        contrast=profile.get('contrast', 1.0),
                        saturation=profile.get('saturation', 1.0)
                    )

                    processed += 1
                    print(f"  Optimized: {filename}")

                except Exception as e:
                    errors += 1
                    print(f"  Error optimizing {filename}: {e}")

            return {'processed': processed, 'errors': errors}

    # Usage
    def create_optimized_image_sets():
        optimizer = ImageOptimizationWorkflow("customtkinter")

        results = optimizer.optimize_folder(
            input_folder="original_images/",
            output_base="optimized_images/",
            profiles=['web_optimized', 'thumbnail', 'icon']
        )

        # Print results
        for profile, result in results.items():
            print(f"{profile}: {result['processed']} processed, {result['errors']} errors")

Batch Processing with Validation
---------------------------------

Quality Control Workflow
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import os
    from pathlib import Path

    class QualityControlBatchProcessor:
        def __init__(self, framework="tkinter"):
            self.framework = framework
            self.validation_rules = {
                'min_size': (100, 100),
                'max_size': (5000, 5000),
                'max_file_size': 10 * 1024 * 1024,  # 10MB
                'allowed_formats': {'.png', '.jpg', '.jpeg', '.gif', '.bmp'}
            }

        def process_with_validation(self, input_folder, output_folder,
                                  transformations, validation_rules=None):
            """Process images with quality validation."""

            if validation_rules:
                self.validation_rules.update(validation_rules)

            # Create output folders
            os.makedirs(output_folder, exist_ok=True)
            rejected_folder = os.path.join(output_folder, '_rejected')
            os.makedirs(rejected_folder, exist_ok=True)

            results = {
                'processed': 0,
                'rejected': 0,
                'errors': 0,
                'rejection_reasons': [],
                'error_list': []
            }

            # Process each file
            for filename in os.listdir(input_folder):
                file_path = os.path.join(input_folder, filename)

                if not os.path.isfile(file_path):
                    continue

                # Validate file
                validation_result = self._validate_file(file_path)

                if not validation_result['valid']:
                    # Move to rejected folder
                    rejected_path = os.path.join(rejected_folder, filename)
                    try:
                        os.rename(file_path, rejected_path)
                        results['rejected'] += 1
                        results['rejection_reasons'].append(
                            f"{filename}: {validation_result['reason']}"
                        )
                        print(f"Rejected: {filename} - {validation_result['reason']}")
                    except Exception as e:
                        results['errors'] += 1
                        results['error_list'].append(f"Failed to reject {filename}: {e}")
                    continue

                # Process valid file
                try:
                    output_path = os.path.join(output_folder, filename)

                    processed_image = get_image(
                        file_path,
                        framework=self.framework,
                        **transformations
                    )

                    results['processed'] += 1
                    print(f"Processed: {filename}")

                except Exception as e:
                    results['errors'] += 1
                    results['error_list'].append(f"{filename}: {str(e)}")
                    print(f"Error processing {filename}: {e}")

            return results

        def _validate_file(self, file_path):
            """Validate a single file against quality rules."""

            filename = os.path.basename(file_path)
            file_ext = Path(filename).suffix.lower()

            # Check file format
            if file_ext not in self.validation_rules['allowed_formats']:
                return {
                    'valid': False,
                    'reason': f"Unsupported format: {file_ext}"
                }

            # Check file size
            try:
                file_size = os.path.getsize(file_path)
                if file_size > self.validation_rules['max_file_size']:
                    return {
                        'valid': False,
                        'reason': f"File too large: {file_size / 1024 / 1024:.1f}MB"
                    }
            except Exception as e:
                return {
                    'valid': False,
                    'reason': f"Cannot read file size: {e}"
                }

            # Additional validations could be added here
            # (image dimensions, corruption check, etc.)

            return {'valid': True, 'reason': None}

    # Usage
    def process_with_quality_control():
        processor = QualityControlBatchProcessor("tkinter")

        # Custom validation rules
        validation_rules = {
            'min_size': (200, 200),
            'max_size': (2000, 2000),
            'max_file_size': 5 * 1024 * 1024,  # 5MB
            'allowed_formats': {'.png', '.jpg', '.jpeg'}
        }

        transformations = {
            'size': (800, 600),
            'contrast': 1.1,
            'saturation': 1.05
        }

        results = processor.process_with_validation(
            input_folder="incoming_images/",
            output_folder="quality_controlled/",
            transformations=transformations,
            validation_rules=validation_rules
        )

        print(f"\nQuality control results:")
        print(f"  Processed: {results['processed']} files")
        print(f"  Rejected: {results['rejected']} files")
        print(f"  Errors: {results['errors']} files")

        if results['rejection_reasons']:
            print("\nRejection reasons:")
            for reason in results['rejection_reasons'][:5]:  # Show first 5
                print(f"  {reason}")

Monitoring and Logging
----------------------

Progress Tracking System
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import time
    import logging
    from datetime import datetime

    class BatchProcessingMonitor:
        def __init__(self, log_file=None):
            self.start_time = None
            self.processed_files = []
            self.failed_files = []
            self.current_file = None

            # Setup logging
            self.logger = logging.getLogger('BatchProcessor')
            self.logger.setLevel(logging.INFO)

            # Console handler
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

            # File handler
            if log_file:
                file_handler = logging.FileHandler(log_file)
                file_handler.setLevel(logging.INFO)
                file_handler.setFormatter(formatter)
                self.logger.addHandler(file_handler)

        def start_batch(self, total_files):
            """Start batch processing monitoring."""
            self.start_time = time.time()
            self.total_files = total_files
            self.processed_files = []
            self.failed_files = []

            self.logger.info(f"Starting batch processing of {total_files} files")

        def file_started(self, file_path):
            """Mark file processing as started."""
            self.current_file = file_path
            self.logger.info(f"Processing: {os.path.basename(file_path)}")

        def file_completed(self, file_path, processing_time=None):
            """Mark file as successfully processed."""
            self.processed_files.append({
                'file': file_path,
                'completed_at': datetime.now(),
                'processing_time': processing_time
            })

            progress = len(self.processed_files) + len(self.failed_files)
            percent = (progress / self.total_files) * 100

            self.logger.info(
                f"Completed: {os.path.basename(file_path)} "
                f"({progress}/{self.total_files} - {percent:.1f}%)"
            )

        def file_failed(self, file_path, error):
            """Mark file as failed."""
            self.failed_files.append({
                'file': file_path,
                'error': str(error),
                'failed_at': datetime.now()
            })

            progress = len(self.processed_files) + len(self.failed_files)
            percent = (progress / self.total_files) * 100

            self.logger.error(
                f"Failed: {os.path.basename(file_path)} - {error} "
                f"({progress}/{self.total_files} - {percent:.1f}%)"
            )

        def finish_batch(self):
            """Finish batch processing and generate report."""
            end_time = time.time()
            total_time = end_time - self.start_time

            report = {
                'total_files': self.total_files,
                'processed': len(self.processed_files),
                'failed': len(self.failed_files),
                'success_rate': (len(self.processed_files) / self.total_files) * 100,
                'total_time': total_time,
                'avg_time_per_file': total_time / self.total_files if self.total_files > 0 else 0
            }

            self.logger.info(f"Batch processing completed:")
            self.logger.info(f"  Total files: {report['total_files']}")
            self.logger.info(f"  Processed: {report['processed']}")
            self.logger.info(f"  Failed: {report['failed']}")
            self.logger.info(f"  Success rate: {report['success_rate']:.1f}%")
            self.logger.info(f"  Total time: {report['total_time']:.1f} seconds")
            self.logger.info(f"  Average time per file: {report['avg_time_per_file']:.2f} seconds")

            return report

    # Usage with monitoring
    def monitored_batch_processing():
        monitor = BatchProcessingMonitor("batch_processing.log")

        input_folder = "images_to_process/"
        output_folder = "processed_images/"

        # Find files
        image_files = []
        for file in os.listdir(input_folder):
            if Path(file).suffix.lower() in {'.png', '.jpg', '.jpeg'}:
                image_files.append(os.path.join(input_folder, file))

        # Start monitoring
        monitor.start_batch(len(image_files))

        transformations = {
            'size': (800, 600),
            'contrast': 1.1,
            'saturation': 1.05
        }

        # Process files with monitoring
        for file_path in image_files:
            file_start_time = time.time()
            monitor.file_started(file_path)

            try:
                # Process image
                processed_image = get_image(
                    file_path,
                    framework="tkinter",
                    **transformations
                )

                processing_time = time.time() - file_start_time
                monitor.file_completed(file_path, processing_time)

            except Exception as e:
                monitor.file_failed(file_path, e)

        # Generate final report
        report = monitor.finish_batch()
        return report

Best Practices for Batch Processing
-----------------------------------

Performance Optimization
~~~~~~~~~~~~~~~~~~~~~~~~~

1. **Use Appropriate Batch Sizes**: Don't process too many files at once
2. **Implement Progress Tracking**: Keep users informed of progress
3. **Handle Errors Gracefully**: Don't let one bad file stop the entire batch
4. **Use Parallel Processing**: When appropriate for large batches

.. code-block:: python

    # Good: Process in chunks
    def process_in_chunks(file_list, chunk_size=50):
        for i in range(0, len(file_list), chunk_size):
            chunk = file_list[i:i + chunk_size]
            process_chunk(chunk)
            # Optional: garbage collection between chunks
            import gc
            gc.collect()

Memory Management
~~~~~~~~~~~~~~~~~

1. **Clear Processed Images**: Don't keep all processed images in memory
2. **Use Generators**: For large file lists
3. **Monitor Memory Usage**: Especially for large images

.. code-block:: python

    # Good: Generator for large file lists
    def image_file_generator(folder):
        for file in os.listdir(folder):
            if Path(file).suffix.lower() in {'.png', '.jpg', '.jpeg'}:
                yield os.path.join(folder, file)

Error Handling
~~~~~~~~~~~~~~

1. **Validate Inputs**: Check files before processing
2. **Log All Errors**: For debugging and reporting
3. **Provide Recovery Options**: Allow resuming failed batches

.. code-block:: python

    # Good: Comprehensive error handling
    def safe_batch_process(file_list, transformations):
        results = {'processed': [], 'failed': []}

        for file_path in file_list:
            try:
                # Validate file first
                if not os.path.exists(file_path):
                    raise FileNotFoundError(f"File not found: {file_path}")

                # Process
                result = get_image(file_path, **transformations)
                results['processed'].append(file_path)

            except Exception as e:
                results['failed'].append({'file': file_path, 'error': str(e)})
                logging.error(f"Failed to process {file_path}: {e}")

        return results

Next Steps
----------

Now that you understand batch operations:

1. **Explore Theme System**: :doc:`theme_system`
2. **Learn Custom Filters**: :doc:`custom_filters`
3. **Try Advanced Examples**: :doc:`../examples/index`
4. **Build Automation Scripts**: :doc:`scripting`
