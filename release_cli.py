import argparse
from release_engine_v2 import DSTerminalReleaseEngineV2


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", default=".")
    parser.add_argument("--tag", default="v0.0.0")
    parser.add_argument("--output", default="RELEASE.md")
    parser.add_argument("--github_token")
    parser.add_argument("--repo_name")

    args = parser.parse_args()

    engine = DSTerminalReleaseEngineV2(
        repo_path=args.repo,
        github_token=args.github_token,
        repo_name=args.repo_name
    )

    version, release_md = engine.run(args.tag)

    with open(args.output, "w", encoding="utf-8") as f:
        f.write(release_md)

    print(f"✅ Version: {version}")
    print(f"📄 Release written to {args.output}")


if __name__ == "__main__":
    main()