import argparse
import hashlib
from email import message_from_bytes
from pathlib import Path
import tarfile


def prepare_source(dist: Path, expected_version: str | None = None) -> dict[str, str]:
    archives = list(dist.glob("*.tar.gz"))
    if len(archives) != 1:
        raise ValueError("Expected exactly one source distribution")
    archive = archives[0].resolve()
    with tarfile.open(archive) as source:
        metadata = [
            member
            for member in source.getmembers()
            if member.isfile()
            and len(Path(member.name).parts) == 2
            and Path(member.name).name == "PKG-INFO"
        ]
        if len(metadata) != 1:
            raise ValueError("Expected one top-level PKG-INFO")
        stream = source.extractfile(metadata[0])
        if stream is None:
            raise ValueError("Cannot read source distribution metadata")
        info = message_from_bytes(stream.read())
    if info["Name"] != "alphalens-reloaded":
        raise ValueError("Source distribution is not alphalens-reloaded")
    version = info["Version"]
    if not version or "\n" in version or "\r" in version:
        raise ValueError("Invalid source distribution version")
    if expected_version and version != expected_version.removeprefix("v"):
        raise ValueError(f"Requested {expected_version}, but source contains {version}")
    return {
        "ALPHALENS_VERSION": version,
        "ALPHALENS_SDIST_URL": archive.as_uri(),
        "ALPHALENS_SDIST_SHA256": hashlib.sha256(archive.read_bytes()).hexdigest(),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("dist", type=Path)
    parser.add_argument("--expected-version")
    parser.add_argument("--github-env", type=Path, required=True)
    args = parser.parse_args()
    values = prepare_source(args.dist, args.expected_version)
    with args.github_env.open("a", encoding="utf-8") as output:
        for name, value in values.items():
            output.write(f"{name}={value}\n")
    print(f"Verified source distribution {values['ALPHALENS_VERSION']}")


if __name__ == "__main__":
    main()
