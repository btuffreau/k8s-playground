#!/usr/bin/env bash

set -euo pipefail

registry_name="${1:-"kind-registry"}"
registry_port="${2:-"5000"}"

cd "$(dirname -- "$0")" || exit 1
cluster_name=$(yq e '.name' aetion-spec.yaml)


function is_kind_cluster_exists(){

  readarray -t clusters < <(kind get clusters)

  for cluster in "${clusters[@]}"; do
    if [ "$cluster" = "$cluster_name" ]; then
      echo "Cluster $cluster_name already exists"
      return 0
    fi
  done
  return 1
}


is_kind_cluster_exists "${cluster_name}" || kind create cluster --config=aetion-spec.yaml
. registry.sh "$registry_name" "$registry_port"