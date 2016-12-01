import time
import signal
from tornado import ioloop


def make_gracefully_shutdown(server, wait_seconds=30,
                             stop_signals=(signal.SIGTERM, signal.SIGQUIT,
                                           signal.SIGINT),
                             logger=None):
    io_loop = server.io_loop or ioloop.IOLoop.instance()

    def stop_handler(signum, frame):
        if logger:
            logger.info("signal received: {}".format(signum))

        def shutdown():
            if logger:
                logger.info("shutdown")

            server.stop()
            deadline = time.time() + wait_seconds

            def stop_loop():
                if logger:
                    logger.info("stop loop: {}".format(
                        (len(io_loop._callbacks), len(io_loop._timeouts))))

                now = time.time()
                if (now < deadline and
                        (len(io_loop._callbacks) > 0 or
                            len(io_loop._timeouts) > 1)):
                    io_loop.add_timeout(now + 1, stop_loop)
                else:
                    io_loop.stop()

            stop_loop()

        io_loop.add_callback_from_signal(shutdown)

    for signum in stop_signals:
        signal.signal(signum, stop_handler)
