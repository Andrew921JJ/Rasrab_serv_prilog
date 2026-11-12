openapi: 3.0.3

info:

  title: Online Chat API

  description: Спецификация REST API для сервиса онлайн-чата (Лабораторная работа #2)

  version: 1.0.0

  

servers:

  - url: http://localhost:8080/api/v1

    description: Локальный сервер разработки

  

paths:

  /auth/login:

    post:

      summary: Вход в систему

      tags:

        - Auth

      requestBody:

        required: true

        content:

          application/json:

            schema:

              $ref: '#/components/schemas/LoginRequest'

      responses:

        '200':

          description: Успешный вход

          content:

            application/json:

              schema:

                $ref: '#/components/schemas/AuthResponse'

        '401':

          description: Неверные учетные данные

          content:

            application/json:

              schema:

                $ref: '#/components/schemas/ErrorResponse'

  

  /rooms:

    get:

      summary: Получение списка чат-комнат

      tags:

        - Rooms

      responses:

        '200':

          description: Список комнат

          content:

            application/json:

              schema:

                type: array

                items:

                  $ref: '#/components/schemas/RoomResponse'

    post:

      summary: Создание новой комнаты

      tags:

        - Rooms

      requestBody:

        required: true

        content:

          application/json:

            schema:

              $ref: '#/components/schemas/CreateRoomRequest'

      responses:

        '201':

          description: Комната создана

          content:

            application/json:

              schema:

                $ref: '#/components/schemas/RoomResponse'

        '400':

          description: Ошибка валидации

          content:

            application/json:

              schema:

                $ref: '#/components/schemas/ErrorResponse'

  

  /rooms/{roomId}/messages:

    get:

      summary: Получение истории сообщений

      tags:

        - Messages

      parameters:

        - name: roomId

          in: path

          required: true

          description: UUID комнаты

          schema:

            type: string

            format: uuid

        - name: limit

          in: query

          description: Количество сообщений (по умолчанию 50)

          required: false

          schema:

            type: integer

            default: 50

      responses:

        '200':

          description: История сообщений

          content:

            application/json:

              schema:

                type: array

                items:

                  $ref: '#/components/schemas/MessageResponse'

    post:

      summary: Отправка сообщения

      tags:

        - Messages

      parameters:

        - name: roomId

          in: path

          required: true

          schema:

            type: string

            format: uuid

      requestBody:

        required: true

        content:

          application/json:

            schema:

              $ref: '#/components/schemas/SendMessageRequest'

      responses:

        '201':

          description: Сообщение отправлено

          content:

            application/json:

              schema:

                $ref: '#/components/schemas/MessageResponse'

        '403':

          description: Нет доступа к комнате

          content:

            application/json:

              schema:

                $ref: '#/components/schemas/ErrorResponse'

  

  /messages/{messageId}:

    delete:

      summary: Удаление сообщения

      tags:

        - Messages

      parameters:

        - name: messageId

          in: path

          required: true

          description: UUID сообщения

          schema:

            type: string

            format: uuid

      responses:

        '204':

          description: Сообщение удалено

        '404':

          description: Сообщение не найдено

          content:

            application/json:

              schema:

                $ref: '#/components/schemas/ErrorResponse'

  

components:

  schemas:

    # --- Request Bodies ---

    LoginRequest:

      type: object

      required:

        - username

        - password

      properties:

        username:

          type: string

          example: "ivan_ivanov"

        password:

          type: string

          format: password

          example: "strongPass123"

  

    CreateRoomRequest:

      type: object

      required:

        - name

      properties:

        name:

          type: string

          example: "Общий чат"

        is_private:

          type: boolean

          default: false

  

    SendMessageRequest:

      type: object

      required:

        - content

      properties:

        content:

          type: string

          example: "Привет, как дела?"

  

    # --- Response Bodies ---

    AuthResponse:

      type: object

      properties:

        access_token:

          type: string

          example: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

        token_type:

          type: string

          example: "Bearer"

        expires_in:

          type: integer

          example: 3600

  

    RoomResponse:

      type: object

      properties:

        id:

          type: string

          format: uuid

          example: "123e4567-e89b-12d3-a456-426614174000"

        name:

          type: string

          example: "Общий чат"

        created_at:

          type: string

          format: date-time

  

    MessageResponse:

      type: object

      properties:

        id:

          type: string

          format: uuid

        room_id:

          type: string

          format: uuid

        sender_id:

          type: string

          format: uuid

        content:

          type: string

        created_at:

          type: string

          format: date-time

  

    # --- Common Error Schema ---

    ErrorResponse:

      type: object

      properties:

        code:

          type: string

          example: "INVALID_INPUT"

        message:

          type: string

          example: "Поле content не может быть пустым"

        timestamp:

          type: string

          format: date-time