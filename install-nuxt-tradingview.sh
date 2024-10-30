#!/bin/bash

is_command_available() {
    command -v "$1" >/dev/null 2>&1
}

if ! is_command_available "nvm"; then
    echo "nvm could not be found, installing..."

    if ! is_command_available "brew"; then
        echo "Homebrew could not be found, installing..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    fi

    brew install nvm
else
    echo "nvm is already installed"
fi

execute_task() {
    eval "$1"
    if [ $? -ne 0 ]; then
        echo "Failed to execute: $1"
        exit 1
    fi
}

get_current_node_version() {
    node -v 2>/dev/null | tr -d '\n'
}

get_nvmrc_version() {
    if [ -f ".nvmrc" ]; then
        cat .nvmrc | tr -d '\n'
    else
        echo ""
    fi
}


get_nvm_version() {
    . ~/.nvm/nvm.sh && nvm --version 2>/dev/null | tr -d '\n'
}

install_node_version() {
    local version=$1
    if . ~/.nvm/nvm.sh && nvm install "$version"; then
        echo "Node.js version $version installed successfully"
    else
        echo "Node.js version $version is already installed, switching with nvm use"
        . ~/.nvm/nvm.sh && nvm use "$version"
    fi
}

install_packages() {
    local current_version=$(get_current_node_version)
    local nvmrc_version=$(get_nvmrc_version)
    local nvm_version=$(get_nvm_version)

    echo "Current NVM version: $nvm_version"
    if [ "$current_version" != "$nvmrc_version" ]; then
        echo "Node.js version mismatch: current version is $current_version but .nvmrc specifies $nvmrc_version"
        install_node_version "$nvmrc_version"
    fi

    if [ ! -d "nuxt-tradingview" ]; then
        execute_task "git clone https://github.com/volkanakkus/nuxt-tradingview.git"
    fi

    execute_task "cd nuxt-tradingview"
    execute_task "npm install"
}

install_packages