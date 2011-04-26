#!/usr/bin/env python

from dev.bootstrap import bootstrap

def main():
    from django.core.management import execute_manager
    import dev.settings
    
    execute_manager(dev.settings)

if __name__ == "__main__":
    bootstrap(main)
