import argparse
import requests
import subprocess
from typing import Dict, List, Optional

class HelmChartManager:
    """Manage Helm charts using Artifact Hub API."""
    
    ARTIFACT_HUB_API = "https://artifacthub.io/api/v1"
    
    def __init__(self):
        """Initialize the Helm Chart Manager."""
        self.session = requests.Session()
    
    def search_charts(self, keyword: str) -> List[Dict]:
        """
        Search for Helm charts in Artifact Hub.
        
        Args:
            keyword: Search term for finding charts
            
        Returns:
            List of charts matching the search term
        """
        url = f"{self.ARTIFACT_HUB_API}/packages/search"
        params = {
            "kind": "0",  # 0 represents Helm charts
            "ts_query": keyword,
            "sort": "relevance"
        }
        
        response = self.session.get(url, params=params)
        response.raise_for_status()
        
        return response.json().get("packages", [])
    
    def get_chart_details(self, name: str) -> Dict:
        """
        Get detailed information about a specific chart.
        
        Args:
            name: Full name of the chart (e.g., bitnami/redis)
            
        Returns:
            Dictionary containing chart details
        """
        # Split repository and chart name
        repo, chart = name.split("/")
        url = f"{self.ARTIFACT_HUB_API}/packages/helm/{repo}/{chart}"
        
        response = self.session.get(url)
        response.raise_for_status()
        
        return response.json()
    
    def add_helm_repo(self, name: str, url: str) -> None:
        """
        Add a Helm repository to local configuration.
        
        Args:
            name: Name of the repository
            url: URL of the repository
        """
        try:
            subprocess.run(["helm", "repo", "add", name, url], check=True)
            subprocess.run(["helm", "repo", "update"], check=True)
        except subprocess.CalledProcessError as e:
            raise Exception(f"Failed to add Helm repository: {str(e)}")
    
    def install_chart(self, name: str, release_name: str, namespace: str = "default", version: Optional[str] = None) -> None:
        """
        Install a Helm chart in the cluster.
        
        Args:
            name: Name of the chart to install
            release_name: Name for the installation
            namespace: Kubernetes namespace
            version: Specific version to install
        """
        cmd = ["helm", "install", release_name, name, "--namespace", namespace]
        if version:
            cmd.extend(["--version", version])
            
        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError as e:
            raise Exception(f"Failed to install chart: {str(e)}")
    
    def list_releases(self, namespace: Optional[str] = None) -> str:
        """
        List all Helm releases in the cluster.
        
        Args:
            namespace: Optional namespace to filter results
            
        Returns:
            String output of helm list command
        """
        cmd = ["helm", "list"]
        if namespace:
            cmd.extend(["-n", namespace])
            
        try:
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            return result.stdout
        except subprocess.CalledProcessError as e:
            raise Exception(f"Failed to list releases: {str(e)}")
    
    def uninstall_release(self, release_name: str, namespace: str = "default") -> None:
        """
        Uninstall a Helm release.
        
        Args:
            release_name: Name of the release to uninstall
            namespace: Namespace where the release is installed
        """
        try:
            subprocess.run(["helm", "uninstall", release_name, "-n", namespace], check=True)
        except subprocess.CalledProcessError as e:
            raise Exception(f"Failed to uninstall release: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description="Manage Helm charts using Artifact Hub")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Search command
    search_parser = subparsers.add_parser("search", help="Search for Helm charts")
    search_parser.add_argument("keyword", help="Keyword to search for")
    
    # Info command
    info_parser = subparsers.add_parser("info", help="Get chart details")
    info_parser.add_argument("name", help="Chart name (e.g., bitnami/redis)")
    
    # Install command
    install_parser = subparsers.add_parser("install", help="Install a chart")
    install_parser.add_argument("name", help="Chart name")
    install_parser.add_argument("--release-name", required=True, help="Name for the release")
    install_parser.add_argument("--namespace", default="default", help="Kubernetes namespace")
    install_parser.add_argument("--version", help="Chart version")
    
    # List releases command
    list_parser = subparsers.add_parser("list-releases", help="List installed releases")
    list_parser.add_argument("--namespace", help="Filter by namespace")
    
    # Uninstall command
    uninstall_parser = subparsers.add_parser("uninstall", help="Uninstall a release")
    uninstall_parser.add_argument("release_name", help="Name of the release to uninstall")
    uninstall_parser.add_argument("--namespace", default="default", help="Release namespace")
    
    args = parser.parse_args()
    manager = HelmChartManager()
    
    try:
        if args.command == "search":
            charts = manager.search_charts(args.keyword)
            for chart in charts[:5]:  # Show top 5 results
                print(f"\nName: {chart['name']}")
                print(f"Repository: {chart['repository']['name']}")
                print(f"Description: {chart['description']}")
                print(f"Version: {chart.get('version', 'N/A')}")
        
        elif args.command == "info":
            details = manager.get_chart_details(args.name)
            print(f"\nName: {details['name']}")
            print(f"Description: {details['description']}")
            print(f"Version: {details.get('version', 'N/A')}")
            print(f"Repository URL: {details['repository']['url']}")
            
        elif args.command == "install":
            manager.install_chart(args.name, args.release_name, args.namespace, args.version)
            print(f"Successfully installed {args.name} as {args.release_name}")
            
        elif args.command == "list-releases":
            print(manager.list_releases(args.namespace))
            
        elif args.command == "uninstall":
            manager.uninstall_release(args.release_name, args.namespace)
            print(f"Successfully uninstalled {args.release_name}")
            
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()