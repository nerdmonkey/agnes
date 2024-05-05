# Agnes API

## About Agnes API
Agnes API is a dynamic platform designed for the agricultural community, providing essential tools and resources to enhance farming operations. It facilitates efficient data exchange and management, supporting farmers in optimizing productivity."This system will manage all nodes in the farm.

## Installation
1. Install all the required packages
```bash
pip install -r requirements.txt
```
2. Copy the .env.example to .env

3. Configure the migration
```bash
spartan migrate init
```

4. Create all the tables
```bash
spartan migrate upgrade
```

5. Insert dummy data
```bash
spartan db seed
```

6. Then run it using the following command
```bash
spartan serve
```

## Usage
1. To install
```bash
pip install python-spartan
```

2. Try
```bash
spartan --help
```

## Testing
```bash
pytest
```

## Changelog

Please see [CHANGELOG](CHANGELOG.md) for more information on what has changed recently.

## Contributing

Please see [CONTRIBUTING](CONTRIBUTING.md) for details.

## Security Vulnerabilities

Please review [our security policy](../../security/policy) on how to report security vulnerabilities.

## Credits

- [Sydel Palinlin](https://github.com/nerdmonkey)
- [All Contributors](../../contributors)

## License

The MIT License (MIT). Please see [License File](LICENSE.md) for more information.
