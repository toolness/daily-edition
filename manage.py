#!/usr/bin/env python

from dev.bootstrap import bootstrap

if __name__ == "__main__":
    bootstrap()

    from django.core.management import execute_manager
    import dev.settings
    
    execute_manager(dev.settings)
