#!/usr/bin/env python3
"""
Verify GitHub Pages deployment for GUI Image Studio documentation.
"""

import sys
import time
from urllib.parse import urljoin

import requests


def check_url(url, timeout=10):
    """Check if a URL is accessible."""
    try:
        response = requests.get(url, timeout=timeout)
        return response.status_code == 200, response.status_code
    except requests.RequestException as e:
        return False, str(e)


def verify_pages_deployment(base_url):
    """Verify that GitHub Pages deployment is working."""

    print(f"🔍 Verifying GitHub Pages deployment at: {base_url}")
    print("=" * 60)

    # Essential pages to check
    pages_to_check = [
        ("Main Page", ""),
        ("API Reference", "api/"),
        ("Installation Guide", "installation.html"),
        ("Quick Start", "quickstart.html"),
        ("Examples", "examples/"),
        ("User Guide", "user_guide/"),
        ("Contributing", "contributing.html"),
        ("Changelog", "changelog.html"),
        ("License", "license.html"),
    ]

    results = []

    for name, path in pages_to_check:
        url = urljoin(base_url.rstrip("/") + "/", path)
        print(f"Checking {name}: {url}")

        success, status = check_url(url)
        results.append((name, url, success, status))

        if success:
            print(f"  ✅ {status}")
        else:
            print(f"  ❌ {status}")

        time.sleep(0.5)  # Be nice to GitHub's servers

    print("\n" + "=" * 60)
    print("📊 SUMMARY")
    print("=" * 60)

    successful = sum(1 for _, _, success, _ in results if success)
    total = len(results)

    print(f"✅ Successful: {successful}/{total}")
    print(f"❌ Failed: {total - successful}/{total}")

    if successful == total:
        print(
            "\n🎉 All pages are accessible! GitHub Pages deployment is working correctly."
        )
        return True
    else:
        print(
            f"\n⚠️ {total - successful} pages are not accessible. This might be normal if:"
        )
        print("   - The deployment is still in progress")
        print("   - Some pages haven't been created yet")
        print("   - There are temporary network issues")

        print("\n📋 Failed pages:")
        for name, url, success, status in results:
            if not success:
                print(f"   - {name}: {url} ({status})")

        return False


def main():
    """Main function."""
    if len(sys.argv) != 2:
        print("Usage: python verify-pages.py <github-pages-url>")
        print(
            "Example: python verify-pages.py https://yourusername.github.io/gui-image-studio/"
        )
        sys.exit(1)

    base_url = sys.argv[1]

    # Ensure URL ends with /
    if not base_url.endswith("/"):
        base_url += "/"

    success = verify_pages_deployment(base_url)

    if success:
        print(f"\n🌐 Your documentation is live at: {base_url}")
        print("💡 You can now share this URL with users and contributors!")
    else:
        print(
            f"\n🔄 If the deployment is still in progress, try again in a few minutes."
        )
        print(
            "📖 Check the Actions tab in your GitHub repository for deployment status."
        )


if __name__ == "__main__":
    main()  #!/usr/bin/env python3
"""
Verify GitHub Pages deployment for GUI Image Studio documentation.
"""

import sys
import time
from urllib.parse import urljoin

import requests


def check_url(url, timeout=10):
    """Check if a URL is accessible."""
    try:
        response = requests.get(url, timeout=timeout)
        return response.status_code == 200, response.status_code
    except requests.RequestException as e:
        return False, str(e)


def verify_pages_deployment(base_url):
    """Verify that GitHub Pages deployment is working."""

    print(f"🔍 Verifying GitHub Pages deployment at: {base_url}")
    print("=" * 60)

    # Essential pages to check
    pages_to_check = [
        ("Main Page", ""),
        ("API Reference", "api/"),
        ("Installation Guide", "installation.html"),
        ("Quick Start", "quickstart.html"),
        ("Examples", "examples/"),
        ("User Guide", "user_guide/"),
        ("Contributing", "contributing.html"),
        ("Changelog", "changelog.html"),
        ("License", "license.html"),
    ]

    results = []

    for name, path in pages_to_check:
        url = urljoin(base_url.rstrip("/") + "/", path)
        print(f"Checking {name}: {url}")

        success, status = check_url(url)
        results.append((name, url, success, status))

        if success:
            print(f"  ✅ {status}")
        else:
            print(f"  ❌ {status}")

        time.sleep(0.5)  # Be nice to GitHub's servers

    print("\n" + "=" * 60)
    print("📊 SUMMARY")
    print("=" * 60)

    successful = sum(1 for _, _, success, _ in results if success)
    total = len(results)

    print(f"✅ Successful: {successful}/{total}")
    print(f"❌ Failed: {total - successful}/{total}")

    if successful == total:
        print(
            "\n🎉 All pages are accessible! GitHub Pages deployment is working correctly."
        )
        return True
    else:
        print(
            f"\n⚠️ {total - successful} pages are not accessible. This might be normal if:"
        )
        print("   - The deployment is still in progress")
        print("   - Some pages haven't been created yet")
        print("   - There are temporary network issues")

        print("\n📋 Failed pages:")
        for name, url, success, status in results:
            if not success:
                print(f"   - {name}: {url} ({status})")

        return False


def main():
    """Main function."""
    if len(sys.argv) != 2:
        print("Usage: python verify-pages.py <github-pages-url>")
        print(
            "Example: python verify-pages.py https://yourusername.github.io/gui-image-studio/"
        )
        sys.exit(1)

    base_url = sys.argv[1]

    # Ensure URL ends with /
    if not base_url.endswith("/"):
        base_url += "/"

    success = verify_pages_deployment(base_url)

    if success:
        print(f"\n🌐 Your documentation is live at: {base_url}")
        print("💡 You can now share this URL with users and contributors!")
    else:
        print(
            f"\n🔄 If the deployment is still in progress, try again in a few minutes."
        )
        print(
            "📖 Check the Actions tab in your GitHub repository for deployment status."
        )


if __name__ == "__main__":
    main()  #!/usr/bin/env python3
"""
Verify GitHub Pages deployment for GUI Image Studio documentation.
"""

import sys
import time
from urllib.parse import urljoin

import requests


def check_url(url, timeout=10):
    """Check if a URL is accessible."""
    try:
        response = requests.get(url, timeout=timeout)
        return response.status_code == 200, response.status_code
    except requests.RequestException as e:
        return False, str(e)


def verify_pages_deployment(base_url):
    """Verify that GitHub Pages deployment is working."""

    print(f"🔍 Verifying GitHub Pages deployment at: {base_url}")
    print("=" * 60)

    # Essential pages to check
    pages_to_check = [
        ("Main Page", ""),
        ("API Reference", "api/"),
        ("Installation Guide", "installation.html"),
        ("Quick Start", "quickstart.html"),
        ("Examples", "examples/"),
        ("User Guide", "user_guide/"),
        ("Contributing", "contributing.html"),
        ("Changelog", "changelog.html"),
        ("License", "license.html"),
    ]

    results = []

    for name, path in pages_to_check:
        url = urljoin(base_url.rstrip("/") + "/", path)
        print(f"Checking {name}: {url}")

        success, status = check_url(url)
        results.append((name, url, success, status))

        if success:
            print(f"  ✅ {status}")
        else:
            print(f"  ❌ {status}")

        time.sleep(0.5)  # Be nice to GitHub's servers

    print("\n" + "=" * 60)
    print("📊 SUMMARY")
    print("=" * 60)

    successful = sum(1 for _, _, success, _ in results if success)
    total = len(results)

    print(f"✅ Successful: {successful}/{total}")
    print(f"❌ Failed: {total - successful}/{total}")

    if successful == total:
        print(
            "\n🎉 All pages are accessible! GitHub Pages deployment is working correctly."
        )
        return True
    else:
        print(
            f"\n⚠️ {total - successful} pages are not accessible. This might be normal if:"
        )
        print("   - The deployment is still in progress")
        print("   - Some pages haven't been created yet")
        print("   - There are temporary network issues")

        print("\n📋 Failed pages:")
        for name, url, success, status in results:
            if not success:
                print(f"   - {name}: {url} ({status})")

        return False


def main():
    """Main function."""
    if len(sys.argv) != 2:
        print("Usage: python verify-pages.py <github-pages-url>")
        print(
            "Example: python verify-pages.py https://yourusername.github.io/gui-image-studio/"
        )
        sys.exit(1)

    base_url = sys.argv[1]

    # Ensure URL ends with /
    if not base_url.endswith("/"):
        base_url += "/"

    success = verify_pages_deployment(base_url)

    if success:
        print(f"\n🌐 Your documentation is live at: {base_url}")
        print("💡 You can now share this URL with users and contributors!")
    else:
        print(
            f"\n🔄 If the deployment is still in progress, try again in a few minutes."
        )
        print(
            "📖 Check the Actions tab in your GitHub repository for deployment status."
        )


if __name__ == "__main__":
    main()
