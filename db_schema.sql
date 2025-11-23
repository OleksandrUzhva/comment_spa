CREATE TABLE comments_comment (
  id serial PRIMARY KEY,
  user_name varchar(50) NOT NULL,
  email varchar(254) NOT NULL,
  homepage varchar(200),
  text text NOT NULL,
  parent_id integer REFERENCES comments_comment (id) ON DELETE CASCADE,
  is_blocked boolean NOT NULL DEFAULT false,
  created_at timestamp with time zone NOT NULL
);
CREATE INDEX comments_comment_created_at_idx ON comments_comment(created_at DESC);