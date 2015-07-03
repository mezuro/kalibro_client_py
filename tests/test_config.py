from nose.tools import assert_equal

import kalibro_client

class TestConfig(object):
    ###########################
    # kalibro_client.config() #
    ###########################

    def test_config(self):
        assert_equal(kalibro_client.config(), kalibro_client.DEFAULT_CONFIG)

    ##############################
    # kalibro_client.configure() #
    ##############################
    #
    # This relies on kalibro_client.config()
    # So if it breaks you should firt look if its unit test is ok

    def test_configure_just_processor_address(self):
        processor_address = 'test_proc'

        kalibro_client.configure(processor_address=processor_address)

        assert_equal(kalibro_client.config()['processor_address'],
                     processor_address)

    def test_configure_just_configurations_address(self):
        configurations_address = 'test_config'

        kalibro_client.configure(configurations_address=configurations_address)

        assert_equal(kalibro_client.config()['configurations_address'],
                     configurations_address)

    def test_configure_with_no_params(self):
        kalibro_client.configure()

        assert_equal(kalibro_client.config(), kalibro_client.DEFAULT_CONFIG)

    def test_configure_with_extra_params(self):
        kalibro_client.configure(test='test')

        assert_equal(kalibro_client.config(), kalibro_client.DEFAULT_CONFIG)

    def test_configure(self):
        processor_address = 'test_proc'
        configurations_address = 'test_config'

        kalibro_client.configure(processor_address=processor_address,
                                 configurations_address=configurations_address)

        assert_equal(kalibro_client.config(),
                     {'processor_address': processor_address,
                     'configurations_address': configurations_address})

    # Ensures that modifications to _config are restored
    def tearDown(self):
        reload(kalibro_client)
