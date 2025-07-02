from unittest.mock import Mock, patch

import pytest

from hostedpi.pi import Pi


def test_pi_init(pi_info, mock_session, api_url):
    pi = Pi(name="test-pi", info=pi_info, api_url=api_url, session=mock_session)
