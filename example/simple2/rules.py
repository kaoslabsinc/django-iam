from iam.utils import override_perms

from simple.models import SimpleProxy
from simple.rules import is_simple_manager

override_perms(SimpleProxy, {
    'view': is_simple_manager,
})
