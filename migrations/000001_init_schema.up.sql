-- 000001_init_schema.up.sql  (MySQL 8.0+)
-- В MySQL DDL не транзакционный (неявный COMMIT), BEGIN/COMMIT не нужны.

-- users
CREATE TABLE users (
    id            CHAR(36)     NOT NULL,
    username      VARCHAR(50)  NOT NULL,
    email         VARCHAR(255) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role          ENUM('user','admin','moderator') NOT NULL DEFAULT 'user',
    bio           TEXT,
    created_at    TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at    TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY uq_users_username (username),
    UNIQUE KEY uq_users_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- categories
CREATE TABLE categories (
    id          INT          NOT NULL AUTO_INCREMENT,
    name        VARCHAR(100) NOT NULL,
    slug        VARCHAR(100) NOT NULL,
    description TEXT,
    PRIMARY KEY (id),
    UNIQUE KEY uq_categories_name (name),
    UNIQUE KEY uq_categories_slug (slug)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- tags
CREATE TABLE tags (
    id   INT         NOT NULL AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY uq_tags_name (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- posts
CREATE TABLE posts (
    id           CHAR(36)     NOT NULL,
    author_id    CHAR(36)     NOT NULL,
    category_id  INT          NULL,
    title        VARCHAR(255) NOT NULL,
    slug         VARCHAR(255) NOT NULL,
    content      LONGTEXT     NOT NULL,
    status       ENUM('draft','published','archived') NOT NULL DEFAULT 'draft',
    published_at TIMESTAMP    NULL DEFAULT NULL,
    created_at   TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at   TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY uq_posts_slug (slug),
    KEY idx_posts_author_id   (author_id),
    KEY idx_posts_category_id (category_id),
    KEY idx_posts_status      (status),
    CONSTRAINT fk_posts_author
        FOREIGN KEY (author_id)   REFERENCES users(id)      ON DELETE CASCADE,
    CONSTRAINT fk_posts_category
        FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- comments (самоссылающаяся иерархия)
CREATE TABLE comments (
    id           CHAR(36) NOT NULL,
    post_id      CHAR(36) NOT NULL,
    user_id      CHAR(36) NOT NULL,
    parent_id    CHAR(36) NULL,
    content      TEXT     NOT NULL,
    is_moderated TINYINT(1) NOT NULL DEFAULT 0,
    created_at   TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    KEY idx_comments_post_id   (post_id),
    KEY idx_comments_user_id   (user_id),
    KEY idx_comments_parent_id (parent_id),
    CONSTRAINT fk_comments_post
        FOREIGN KEY (post_id)   REFERENCES posts(id)    ON DELETE CASCADE,
    CONSTRAINT fk_comments_user
        FOREIGN KEY (user_id)   REFERENCES users(id)    ON DELETE CASCADE,
    CONSTRAINT fk_comments_parent
        FOREIGN KEY (parent_id) REFERENCES comments(id) ON DELETE CASCADE,
    CONSTRAINT chk_comments_no_self
        CHECK (parent_id IS NULL OR parent_id <> id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- post_tags (M:N)
CREATE TABLE post_tags (
    post_id CHAR(36) NOT NULL,
    tag_id  INT      NOT NULL,
    PRIMARY KEY (post_id, tag_id),
    KEY idx_post_tags_tag_id (tag_id),
    CONSTRAINT fk_post_tags_post
        FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE,
    CONSTRAINT fk_post_tags_tag
        FOREIGN KEY (tag_id)  REFERENCES tags(id)  ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;