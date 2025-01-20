#
# This file is part of the C2_treatment_nonmaleficence_valuator distribution
# (https://github.com/VALAWAI/C2_treatment_nonmaleficence_valuator).
# Copyright (c) 2022-2026 VALAWAI (https://valawai.eu/).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.	If not, see <http://www.gnu.org/licenses/>.
#

import json
import logging
import os
import time
from threading import Thread

import pika


class _RabbitMQConnection:

	def __init__(self,
		host:str=os.getenv('RABBITMQ_HOST','mov-mq'),
		port:int=int(os.getenv('RABBITMQ_PORT',"5672")),
		username:str=os.getenv('RABBITMQ_USERNAME','mov'),
		password:str=os.getenv('RABBITMQ_PASSWORD','password'),
		max_retries:int=int(os.getenv('RABBITMQ_MAX_RETRIES',"100")),
		retry_sleep_seconds:int=int(os.getenv('RABBITMQ_RETRY_SLEEP',"3")),
	):
		"""Initialize the connection to the RabbitMQ

		Parameters
		----------
		host : str
			The RabbitMQ server host name. By default uses the environment variable RABBITMQ_HOST
			and if it is not defined uses 'mov-mq'.
		port : int
			The RabbitMQ server port. By default uses the environment variable RABBITMQ_PORT
			and if it is not defined uses '5672'.
		username : str
			The user name of the credential to connect to the RabbitMQ serve. By default uses the environment
			variable RABBITMQ_USERNAME and if it is not defined uses 'mov'.
		password : str
			The password of the credential to connect to the RabbitMQ serve. By default uses the environment
			variable RABBITMQ_PASSWORD and if it is not defined uses 'password'.
		max_retries : int
			The number maximum of tries to create a connection with the RabbitMQ server. By default uses
			the environment variable RABBITMQ_MAX_RETRIES and if it is not defined uses '100'.
		retry_sleep_seconds : int
			The seconds to wait between the tries for create a connection with the RabbitMQ server.
			By default uses the environment variable RABBITMQ_RETRY_SLEEP and if it is not defined uses '3'.
		"""

		tries=0
		while tries < max_retries:

			try:

				credentials = pika.PlainCredentials(username=username,password=password)
				self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=host,port=port,credentials=credentials))
				self.channel = self.connection.channel()

			except (OSError,pika.exceptions.AMQPError):

				logging.warning("Connection was closed, retrying...")
				time.sleep(retry_sleep_seconds)

			else:

				return

			tries+=1

		error_msg = "Cannot connect with the RabbitMQ"
		logging.error(error_msg)
		raise pika.exceptions.AMQPError(error_msg)

	def close(self):
		"""Close the connection."""

		try:

			if self.connection.is_open is True:

				self.channel.stop_consuming()
				self.connection.close()

		except (OSError,pika.exceptions.AMQPError):

			logging.exception("Cannot close the connection.")


class MessageService:
	"""The service to send and receive messages from the RabbitMQ"""

	def __init__(self,
			host:str=os.getenv('RABBITMQ_HOST','mov-mq'),
			port:int=int(os.getenv('RABBITMQ_PORT',"5672")),
			username:str=os.getenv('RABBITMQ_USERNAME','mov'),
			password:str=os.getenv('RABBITMQ_PASSWORD','password'),
			max_retries:int=int(os.getenv('RABBITMQ_MAX_RETRIES',"100")),
			retry_sleep_seconds:int=int(os.getenv('RABBITMQ_RETRY_SLEEP',"3")),
		):
		"""Initialize the connection to the RabbitMQ

		Parameters
		----------
		host : str
			The RabbitMQ server host name. By default uses the environment variable RABBITMQ_HOST
			and if it is not defined uses 'mov-mq'.
		port : int
			The RabbitMQ server port. By default uses the environment variable RABBITMQ_PORT
			and if it is not defined uses '5672'.
		username : str
			The user name of the credential to connect to the RabbitMQ serve. By default uses the environment
			variable RABBITMQ_USERNAME and if it is not defined uses 'mov'.
		password : str
			The password of the credential to connect to the RabbitMQ serve. By default uses the environment
			variable RABBITMQ_PASSWORD and if it is not defined uses 'password'.
		max_retries : int
			The number maximum of tries to create a connection with the RabbitMQ server. By default uses
			the environment variable RABBITMQ_MAX_RETRIES and if it is not defined uses '100'.
		retry_sleep_seconds : int
			The seconds to wait between the tries for create a connection with the RabbitMQ server.
			By default uses the environment variable RABBITMQ_RETRY_SLEEP and if it is not defined uses '3'.
		"""

		try:

			self.listen_connection = _RabbitMQConnection(host=host,port=port,username=username,password=password,max_retries=max_retries,retry_sleep_seconds=retry_sleep_seconds)
			logging.debug("Opened Listening connection to RabbitMQ")

		except pika.exceptions.AMQPError as listen_error:

			error_msg = f"Cannot listen from the RabbitMQ at {host}:{port}"
			raise ValueError(error_msg) from listen_error

		try:


			self.publish_connection = _RabbitMQConnection(host=host,port=port,username=username,password=password,max_retries=max_retries,retry_sleep_seconds=retry_sleep_seconds)
			logging.debug("Opened publish connection to RabbitMQ")

		except pika.exceptions.AMQPError as publish_error:

			try:

				self.listen_connection.close()

			except pika.exceptions.AMQPError:

				logging.exception("Cannot close the listening connection to RabbitMQ")

			error_msg = f"Cannot connect from the RabbitMQ at {host}:{port}"
			raise ValueError(error_msg) from publish_error


	def close(self):
		"""Close the connections."""

		try:

			self.listen_connection.close()
			self.publish_connection.close()

		except pika.exceptions.AMQPError:

			logging.exception("Cannot close the connection to RabbitMQ")

		except BaseException:

			logging.exception("Unexpected close RabbitMQ connection status")



	def listen_for(self,queue:str,callback):
		"""Register a input channel

		Parameters
		----------
		queue : str
			The name of the queue to listen.
		callback: method
			The method to call when a message is received.
		"""

		self.listen_connection.channel.queue_declare(queue=queue,
			durable=True,
			exclusive=False,
			auto_delete=False)
		self.listen_connection.channel.basic_consume(queue=queue,
			auto_ack=True,
			on_message_callback=callback)
		logging.debug("Listen for the queue %s",queue)


	def publish_to(self,queue:str,msg):
		"""Register a input channel

		Parameters
		----------
		queue : str
			The name of the queue to publish the event.
		msg: object
			The message to send.
		"""

		try:

			body=json.dumps(msg)
			properties=pika.BasicProperties(content_type='application/json')
			self.publish_connection.channel.basic_publish(exchange='',routing_key=queue,body=body,properties=properties)
			logging.debug("Publish message to the queue %s",queue)

		except pika.exceptions.AMQPError:

			logging.exception("Cannot publish a msg in the queue %s",queue)

		except ValueError:

			logging.exception("Cannot publish a msg because can not encode the message")


	def start_consuming(self):
		"""Start to consume the messages."""

		try:

			logging.info("Start listening for events")
			self.listen_connection.channel.start_consuming()

		except KeyboardInterrupt:

			logging.info("Stop listening for events")

		except pika.exceptions.AMQPError:

			logging.info("Closed connection")

		except BaseException:

			logging.exception("Consuming messages error.")

	def start_consuming_and_forget(self):
		"""Start to consume the messages using an independent Thread."""

		Thread(target=self.start_consuming).start()
