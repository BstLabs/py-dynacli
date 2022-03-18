"""
Awesome
"""

# This will be ignored as well as it does not come from the search_path/root_package
from os.path import join
from typing import Type

# This imported function should be ignored as it is not from the public path
from .._common.session import get_session
from ..feature_A.feature_B.create import create
from .feature_F import service
from .feature_F.service import new


# So you can use any kind of common functionality here.
# We consider the imported functionality as nested feature commands if it came from public path.
# Otherwise, it will be ignored and will not be exposed in CLI.
def _use_session():
    get_session("fake session")
