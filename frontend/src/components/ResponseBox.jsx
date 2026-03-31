export default function ResponseBox({ title, data }) {
  if (!data) return null;
  return (
    <div className="card">
      <h2>{title}</h2>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  );
}
